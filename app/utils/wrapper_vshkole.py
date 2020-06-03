import httpx

from app.models.user import User
from app.utils.httpx import httpx_worker

classes = {
    "1": 11,
    "2": 10,
    "3": 9,
    "4": 8,
    "5": 1,
    "6": 2,
    "7": 3,
    "8": 4,
    "9": 5,
    "10": 6,
    "11": 7,
}


class Wrapper:
    API_SUBJECTS = (
        "https://vshkole.com/api/get_class_subjects?new-app=1&class_id={}&type=ab"
    )
    API_SUBJECT_ENTITIES = "https://vshkole.com/api/get_subject_class_entities?new-app=1&class_id={}&subject_id={}&type=ab"
    API_ENTITIE = "https://vshkole.com/api/get_entity_by_id?new-app=1&id={}&type=ab"

    def __init__(
        self,
        class_: int = None,
        subject: str = None,
        subjects=None,
        subject_entities=None,
        author=None,
        specification=None,
        year=None,
        book_id=None,
        entities=None,
        main_topic=None,
        sub_topic=None,
        sub_sub_topic=None,
        exercise=None,
        solution_id=None,
    ):
        self._class = class_
        self._subject = subject
        self._subjects = subjects
        self._subject_entities = subject_entities
        self._author = author
        self._specification = specification
        self._year = year
        self._book_id = book_id
        self._entities = entities
        self._main_topic = main_topic
        self._sub_topic = sub_topic
        self._sub_sub_topic = sub_sub_topic
        self._exercise = exercise
        self._solution_id = solution_id
        self._client = httpx.AsyncClient()

    # init private methods
    async def _close_client(self):
        await self._client.aclose()

    async def _get_data(self, url):
        r = await self._client.get(url)
        return r.json()

    # init properties
    @property
    def class_(self):
        return classes[str(self._class)]

    @class_.setter
    def class_(self, class_):
        self._class = class_

    @property
    def subject(self):
        for i in self._subjects:
            if i["name"] == self._subject:
                return i["id"]

    @subject.setter
    def subject(self, subject):
        self._subject = subject

    @property
    def author(self):
        return "".join(i for i in self._author.lower() if i.isalpha())

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def specification(self):
        return self._specification

    @specification.setter
    def specification(self, value):
        if value == "Підручник":
            value = ""
        self._specification = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def book_id(self):
        if not self._book_id:
            for entitie in self._subject_entities:
                auth = self.lower_author(entitie["authors"])
                specification = entitie["specification"]
                year = int(entitie["year"])
                if (
                    auth == self.author
                    and specification == self.specification
                    and (not self.year or self.year == year)
                ):
                    book_id = entitie["id"]
        else:
            book_id = self._book_id
        return book_id

    @property
    def main_topic(self):
        return self._main_topic

    @main_topic.setter
    def main_topic(self, value):
        self._main_topic = value

    @property
    def sub_topic(self):
        return self._sub_topic

    @sub_topic.setter
    def sub_topic(self, value):
        self._sub_topic = value

    @property
    def sub_sub_topic(self):
        return self._sub_sub_topic

    @sub_sub_topic.setter
    def sub_sub_topic(self, value):
        self._sub_sub_topic = value

    @property
    def exercise(self):
        return self._exercise

    @exercise.setter
    def exercise(self, value):
        self._exercise = value

    @property
    def solution_id(self):
        return self._solution_id

    @solution_id.setter
    def solution_id(self, value):
        self._solution_id = value

    # main methods
    async def subjects(self):
        url = self.API_SUBJECTS.format(self.class_)
        data = await self._get_data(url)
        return data

    async def subject_entities(self):
        url = self.API_SUBJECT_ENTITIES.format(self.class_, self.subject)
        data = await self._get_data(url)
        return data

    async def authors(self):
        self._subject_entities = await self.subject_entities()
        uni_authors = []
        used_authors = []

        for entitie in self._subject_entities:
            auth = entitie["authors"]
            lower_author = self.lower_author(auth)
            if lower_author not in used_authors:
                uni_authors.append(auth.strip())
                used_authors.append(lower_author.strip())
        return uni_authors

    async def specifications(self):
        specifications = []

        for entitie in self._subject_entities:
            auth = self.lower_author(entitie["authors"])
            specification = entitie["specification"]
            if not specification:
                specification = "Підручник"
            if self.author == auth and specification not in specifications:
                specifications.append(specification.strip())
        return specifications

    async def years(self):
        years = []

        for entitie in self._subject_entities:
            auth = self.lower_author(entitie["authors"])
            specification = entitie["specification"].strip()
            year = entitie["year"]
            if self.author == auth and self.specification == specification:
                years.append(year.strip())
        return years

    async def entities(self):
        url = self.API_ENTITIE.format(self.book_id)
        data = await self._get_data(url)
        return data

    async def main_topics(self):
        self._entities = await self.entities()
        return [entitie["name"].strip() for entitie in self._entities["contents"]]

    async def sub_topics(self):
        return [
            i["name"]
            for i in self.get_child(self._entities["contents"], (self.main_topic,))
            if i.get("__children")
        ]

    async def sub_sub_topics(self):
        return [
            i["name"]
            for i in self.get_child(
                self._entities["contents"], (self.main_topic, self.sub_topic)
            )
            if i.get("__children")
        ]

    async def exercises(self):
        return [
            i["name"]
            for i in self.get_child(
                self._entities["contents"],
                (self.main_topic, self.sub_topic, self.sub_sub_topic),
            )
        ]

    async def solution(self):
        solutions = list(
            self.get_child(
                self._entities["contents"],
                (self.main_topic, self.sub_topic, self.sub_sub_topic, self.exercise),
            )
        )[0]
        self.solution_id = solutions["id"]
        return solutions["image_urls"][0]

    # init static methods
    @staticmethod
    def lower_author(author):
        return "".join(i for i in author.lower() if i.isalpha())

    def get_child(self, data, path):
        path = [i for i in path if i]
        topic = path[0]
        for child in data:
            if topic is None:
                yield child
            else:
                if child["name"].strip() == topic or (
                    topic[-1] == "…" and child["name"].startswith(topic[:-1])
                ):
                    grandchildren = child.get("__children")
                    if len(path) > 1:
                        yield from self.get_child(grandchildren, path[1:])
                    else:
                        if not grandchildren:
                            yield child
                        else:
                            yield from grandchildren


class Wrapper_for_bot(Wrapper):
    def __init__(self, user: User, **kwargs):
        self._user = user
        self._client = httpx_worker
        super().__init__(**kwargs)

    async def subjects(self):
        self.class_ = self._user.class_
        return await super().subjects()

    async def authors(self):
        self.class_ = self._user.class_
        self.subject = self._user.subject
        authors = await super().authors()
        entities = self._subject_entities
        return authors, entities

    async def specifications(self):
        self.author = self._user.author
        specifications = await super().specifications()
        return specifications

    async def years(self):
        self.author = self._user.author
        self.specification = self._user.specification
        years = await super().years()
        return years

    async def main_topics(self):
        self.author = self._user.author
        self.specification = self._user.specification
        self.year = self._user.year
        main_topics = await super().main_topics()
        entities = self._entities
        return main_topics, entities

    async def sub_topics(self):
        self.main_topic = self._user.main_topic
        sub_topics = await super().sub_topics()
        return sub_topics

    async def sub_sub_topics(self):
        self.main_topic = self._user.main_topic
        self.sub_topic = self._user.sub_topic
        sub_sub_topics = await super().sub_sub_topics()
        return sub_sub_topics

    async def exercises(self):
        self.main_topic = self._user.main_topic
        self.sub_topic = self._user.sub_topic
        self.sub_sub_topic = self._user.sub_sub_topic
        exercises = await super().exercises()
        return exercises

    async def solution(self):
        self.main_topic = self._user.main_topic
        self.sub_topic = self._user.sub_topic
        self.sub_sub_topic = self._user.sub_sub_topic
        self.exercise = self._user.exercise
        solution_url = await super().solution()
        solution_id = self.solution_id
        return solution_id, solution_url
