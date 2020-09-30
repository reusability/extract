import requests
from bs4 import BeautifulSoup
import re as regex


class Maven_Crawler:
    # class that crawls popular Maven projects.
    def __init__(self, category="popular"):
        self.base_url = "https://mvnrepository.com"
        self.category = category
        self.page = 1

    def list_projects(self) -> []:
        """
        Crawl the list of Maven project in the given category
        :return: [{'link': link to maven project, 'usage': total usage of the project},,,,]
        """
        # return value
        projects_urls: [] = []

        # load page with current count (self.page)
        page = requests.get(
            "{}/{}?p={}".format(self.base_url, self.category, self.page)
        )
        if page.status_code == 404:
            return projects_urls
        # load html page
        html_page = BeautifulSoup(page.content, "html.parser")

        content = html_page.find("div", attrs={"id": "maincontent"})

        # get all tags that stores projects info
        projects = content.find_all("div", attrs={"class": "im"})
        # for each project listed
        for project in projects:
            # get the url for a project
            path = project.find("a")["href"]
            # get total usage of a project
            usage = (
                project.find("h2", attrs={"class": "im-title"})
                .find("a", attrs={"class": "im-usage"})
                .find("b")
            )
            # construct the valid url
            project_info = {"link": self.base_url + path, "usage": usage.contents[0]}
            projects_urls.append(project_info)

        # increase page number for check the next list in the next call of this method
        self.page += 1
        return projects_urls

    @staticmethod
    def get_GH_url(maven_project) -> str:
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
                pat = regex.compile("[git|http].*github\.com.*<")  # noqa : W605
                all_urls = regex.findall(pat, xml_content)

                # remove the `<` symbol
                all_urls = [x[:-1] for x in all_urls]

                # for each matched result
                for url in all_urls:
                    # if the matched contains `@git`
                    at_git = regex.search("git@github.com", url)
                    if at_git:
                        url = url.replace(":", "/")
                        end_git = regex.search("\.git", url)  # noqa : W605
                        add_https = (
                            "https://github.com"
                            + url[at_git.end() : end_git.end()]  # noqa : E203
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

                    # if last part of the url appears in the maven_project
                    if last_part in project_name.split("/"):
                        check_start = regex.search("http", url)
                        if check_start:
                            url = url[check_start.start() :]  # noqa : E203
                        return url + ".git"

                return "None"


def crawl_maven_project(project_url):
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
