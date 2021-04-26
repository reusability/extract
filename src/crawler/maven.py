import re as regex
import time

import requests
from bs4 import BeautifulSoup

from src.crawler.index import Crawler, EXCLUSION_LIST
from src.utils import Logger


class MavenCrawler(Crawler):
    # class that crawls popular Maven projects.
    def __init__(self, sleep, logger: Logger, categories=None):
        super().__init__()
        self.base_url = "https://mvnrepository.com"
        self.sleep = sleep
        self.logger = logger
        if categories:
            self.categories = categories
        else:
            self.categories = self._get_categories()
        self.number_categories = len(self.categories)
        self.page = 1
        self.current_category = 0

    def _get_categories(self):
        # TODO: make this abstract to be used with project_list crawler
        curr_page = 1
        suffix = "open-source"
        categories = []
        while True:
            page = requests.get("{}/{}?p={}".format(self.base_url, suffix, curr_page))

            if page.status_code == 404:
                return categories

            html_page = BeautifulSoup(page.content, "html.parser")
            content = html_page.find("div", attrs={"id": "maincontent"})

            # print(html_page)

            list_categories = content.find_all("h4")

            if len(list_categories) == 0:
                return categories

            for category in list_categories:
                path = category.find("a")["href"][1:]
                if path not in EXCLUSION_LIST:
                    categories.append(path)

            curr_page += 1
            time.sleep(self.sleep)

    def _request_page(self):
        try:
            # load page with current count (self.page)
            page = requests.get(
                "{}/{}?p={}".format(
                    self.base_url, self.categories[self.current_category], self.page
                )
            )

            # load html page
            html_page = BeautifulSoup(page.content, "html.parser")

            content = html_page.find("div", attrs={"id": "maincontent"})
            # get all tags that stores projects info
            projects = content.find_all("div", attrs={"class": "im"})
        except:  # noqa : E722
            projects = []

        return projects

    def list_projects(self) -> []:
        """
        Crawl the list of Maven project in the given category
        :return: [{'link': link to maven project, 'usage': total usage of the project},,,,]
        """
        # return value
        projects_urls: [] = []

        projects = self._request_page()

        if len(projects) == 0:
            self.current_category += 1
            if self.current_category >= self.number_categories:
                return projects_urls
            else:
                # TODO move this duplicated code
                # load page with current count (self.page) after pointing to the next category
                self.page = 1
                projects = self._request_page()

        # for each project listed
        for project in projects:
            # get the url for a project
            path = project.find("a")["href"]
            try:
                # get total usage of a project
                usage = (
                    project.find("h2", attrs={"class": "im-title"})
                    .find("a", attrs={"class": "im-usage"})
                    .find("b")
                    .contents[0]
                )

            except:  # noqa : E722
                usage = "0"

            # construct the valid url
            project_info = {
                "link": self.base_url + path,
                "usage": usage.replace(",", ""),
            }
            projects_urls.append(project_info)

        # increase page number for check the next list in the next call of this method
        self.page += 1
        return projects_urls

    @staticmethod
    def get_GH_url(maven_project) -> str:  # noqa : C901
        """
        This method is used to retrieve Github link of a given Maven project by accessing the .pom file of one of the
        releases
        :param maven_project:
        :return: github_link or None
        """

        # maven_project example: https://mvnrepository.com/artifact/junit/junit

        # this path is used when getting the .pom file
        prefix = "https://repo1.maven.org/maven2"

        # get all releases details
        data = crawl_maven_project(maven_project)
        # for each release
        for key, value in data.items():
            for minor in data[key]["releases"]:
                # Construct .pom path:
                # 1: get project name from the link of a release
                org_name = minor["link"].split("/")[-2]
                # 2: get all parts after the `artifact` in the maven_project url
                # 3: some projects in maven_project they use `.` instead of `/`
                project_name = maven_project.split("artifact")[-1].replace(".", "/")
                # 4: concatenate everything and prepend `prefix`
                pom_file = "{}{}/{}/{}-{}.pom".format(
                    prefix, project_name, minor["release"], org_name, minor["release"]
                )
                # load the .pom file based on the constructed url
                content = requests.get(pom_file)

                if content.status_code == 404:
                    # in some cases like in scalajs, some other format is followed
                    modified_project_name = "/".join(project_name.split("/")[:-1])
                    pom_file = "{}{}/{}/{}/{}-{}.pom".format(
                        prefix,
                        modified_project_name,
                        org_name,
                        minor["release"],
                        org_name,
                        minor["release"],
                    )
                    content = requests.get(pom_file)

                xml_content = str(BeautifulSoup(content.content, "lxml"))

                # get everything starts with `git or http` and ends with `.com<`
                pat = regex.compile(">[git|http].*github\.com.*<")  # noqa : W605
                all_urls = regex.findall(pat, xml_content)

                all_urls = [x.split(">") for x in all_urls]
                all_urls = [
                    item for sublist in all_urls for item in sublist if (len(item) > 3)
                ]
                # remove the `<` symbol
                for x in range(len(all_urls)):
                    if all_urls[x][0] == ">":
                        all_urls[x] = all_urls[x][1:]
                    if all_urls[x][-1] == "<":
                        all_urls[x] = all_urls[x][:-1]

                # for each matched result
                for url in all_urls:

                    # remove /tree/master
                    tree_master = regex.search("/tree/master", url)
                    if tree_master:
                        url = url[: tree_master.start()]
                        return url + ".git"

                    # if the matched contains `@git`
                    at_git = regex.search("git@github.com", url)
                    if at_git:
                        url = url.replace(":", "/")
                        end_git = regex.search("\.git", url)  # noqa : W605
                        if end_git:
                            add_https = (
                                "https://github.com"
                                + url[at_git.end() : end_git.end()]  # noqa : E203
                            )
                        else:
                            add_https = (
                                "https://github.com"
                                + url[at_git.end() :]  # noqa : E203
                            )
                        return add_https

                    # if the matched url ends with `.git`
                    end_git = regex.search(r"^https://.*.git$", url)
                    if end_git:
                        return url

                    # if the matched url is for GH issues url
                    issue = regex.search(r"/issues", url)
                    if issue:
                        return url[: issue.start()] + ".git"

                    # last part matches org name
                    if url[-1] == "/":
                        url = url[:-1]
                    last_part = url.split("/")[-1]
                    project_name_check = project_name.split("/")[-1]

                    # this when names are close to each other: eg: mongo-java-driver and mongo-scala-driver
                    possible_match = 0
                    for i in last_part.split("-"):
                        if i in project_name_check.split("-"):
                            possible_match += 1

                    # if last part of the url is same as organization name
                    if last_part in project_name_check or (
                        possible_match / len(last_part.split("-")) > 0.5
                    ):
                        check_start = regex.search("http", url)
                        if check_start:
                            url = url[check_start.start() :]  # noqa : E203
                            return url + ".git"

                return "None"


def crawl_maven_project(project_url):  # noqa : C901
    """
    This function is used to get Maven usage of all releases of a given project.

    :param project_url: path to maven project page. e.g: https://mvnrepository.com/artifact/junit/junit
    :return: dictionary contains :
        { major_1: {
                  releases: [{minor: '', link: '', usage: '', date: ''},,,,,]},
          major_2: {
                  releases: [{minor: '', link: '', usage: '', date: ''},,,,,]},
        }
    """
    page = requests.get(project_url)
    # load html page
    soup = BeautifulSoup(page.content, "html.parser")

    data = {}
    table = soup.find("table", attrs={"class": "grid versions"})
    table_body = table.find_all("tbody")

    # loop over the releases table: for each major release
    for t in table_body:
        rows = t.find_all("tr")
        main_release = ""
        # for each minor release
        for row in rows:
            cols = row.find_all("td")
            minor = {}
            # for each cell in the row
            for element in cols:
                # this is used to find major release 1.1.x
                row_span = element.find("div")
                # this is used to find minor release link
                element_a = element.find("a")
                # this is used to find number of usages
                usage = element.find("span", attrs={"class": "rb"})
                cell_data = element.text.strip()

                if row_span:
                    main_release = cell_data
                    data[main_release] = {"releases": []}
                    minor = {}

                elif usage:
                    usage = element.text.strip()
                    minor["usage"] = usage
                elif element_a:
                    if element_a["class"][0] in ["vsc", "vbtn"]:
                        link = element_a["href"]
                        minor["release"] = link.split("/")[-1]
                        minor["link"] = link
                else:
                    date = cell_data
                    minor["date"] = date
                    # some of projects does not have major release
                    if main_release == "":
                        main_release = "no main release"

                    try:
                        data[main_release]["releases"].append(minor)
                    except:  # noqa : E722
                        data[main_release] = {"releases": []}
                        data[main_release]["releases"].append(minor)

    return data
