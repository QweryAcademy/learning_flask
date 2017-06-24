from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_
from flask_login import UserMixin
db = SQLAlchemy()


class SaveMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class SearchCounter(SaveMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer)
    result_id = db.Column(db.Integer, db.ForeignKey('search_result.id'))

    def increment(self):
        self.counter += 1  # self.counter = self.counter+1
        self.save()


class SearchResult(SaveMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String())
    url = db.Column(db.String())

    def __repr__(self):
        return "<SearchResult :%s>" % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def counter(self):
        result = SearchCounter.query.filter(
            SearchCounter.result_id == self.id).first()
        if result:
            return result
        result = SearchCounter(result_id=self.id, counter=0)
        return result.save()

    @classmethod
    def populate_data(cls):
        data = {
            'title': "Google Drive (@googledrive) · Twitter",
            "url": "https://twitter.com/googledrive",
            "content": """
        <div class="st">
            <div class="_Czh _HOh r-izzCwYuaC_j8" jsl="$t t-_Q_gSb1oLyw;$x 0;">
                <g-inner-card class="_dCh">
                    <!--m-->
                    <div class="tw-res" data-ved="0ahUKEwjh54ihl4TUAhWBrRoKHXxrClcQ_VMIPigAMAk">
                        <div class="_xAh _AOf" aria-level="3" role="heading">For info on how to recover lost files after a malware attack, read here: <a></a><a class="_Lgi" href="https://goo.gl/jlZthd"
                                onmousedown="return rwt(this,'','','','10','AFQjCNF_D6xBRE2gUeaJIcolxwDKa866zA','MGORzmi3YvFG-ugp5Q3COw','0ahUKEwjh54ihl4TUAhWBrRoKHXxrClcQhlQIPzAJ','','',event)">goo.gl/jlZthd</a>.
                            <a></a><a class="_Lgi" href="https://twitter.com/googledrive/status/865670141643702273/photo/1"
                                onmousedown="return rwt(this,'','','','10','AFQjCNE-9PGvqCM0z2lRL4wSxmqX_Et-IQ','aDjSUb4B2oGmGGdchemcyw','0ahUKEwjh54ihl4TUAhWBrRoKHXxrClcQhlcIQDAJ','','',event)">pic.twitter.com/mYi07TC…</a></div>
                        <div class="_yAh">
                            <div><span class="f">3 days ago</span><span class="f"> · </span>
                                <g-link><a href="https://twitter.com/googledrive/status/865670141643702273?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Etweet"
                                        onmousedown="return rwt(this,'','','','10','AFQjCNGYB46oLZ2cNGkS4Q0etSxacidfaQ','XI5QMdsiF1GlhIh4swzIiw','0ahUKEwjh54ihl4TUAhWBrRoKHXxrClcQglQIQTAJ','','',event)">Twitter</a></g-link>
                            </div>
                        </div>
                    </div>
                    <!--n-->
                </g-inner-card>
            </div>
        </div>"""
        }
        # instance = cls(title=data['title'],
        #                url=data['url'], content=data['content'])
        instance = cls(**data)
        instance.save()

    @classmethod
    def get_result(cls, search_param=None):
        query = cls.query
        if search_param:
            search_query = "%{}%".format(search_param)
            title_query = cls.title.ilike(search_query)
            content_query = cls.content.ilike(search_query)
            query = query.filter(or_(title_query, content_query)).all()
        else:
            query = []
        for i in query:
            i.counter.increment()
        return query


class User(UserMixin, SaveMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
