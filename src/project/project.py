# project.py
class Project:
    def __init__(self, name, maven, github, tags):
        self.name = name
        self.maven: str = maven
        self.github: str = github
        self.tags: [] = tags


class Projects:
    def __init__(self, projects: [Project]):
        self.projects: [Project] = projects


scala: Project = Project(
    "scala",
    "https://mvnrepository.com/artifact/org.scala-lang/scala-library",
    "https://github.com/scala/scala",
    ["2.12.12", "2.13.3", "2.13.2"],
)

gson: Project = Project(
    "gson",
    "https://mvnrepository.com/artifact/com.google.code.gson/gson",
    "https://github.com/google/gson",
    ["2.8.6", "2.8.5", "2.8.4"],
)

projects: Projects = Projects([scala, gson])
