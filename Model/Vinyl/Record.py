from .Track import Track
from ..ModelBase import *
from .Associations import AscSubGenre, AscGenre, AscSellerRecord


@dataclass()
class Record(ModelBase, Base):
    """
    A class that holds the Article properties

    """
    __tablename__ = 'record'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    artist: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column()
    # todo: reviews?
    # lazy = "joined" : each Parent will also have its children collection populated
    tracks: Mapped[List[Track]] = relationship("Track", lazy="joined", cascade="all, delete")
    genres: Mapped[List[AscGenre]] = relationship(lazy="joined", cascade="all, delete")
    sub_genres: Mapped[List[AscSubGenre]] = relationship(lazy="joined", cascade="all, delete")
    seller: Mapped[List[AscSellerRecord]] = relationship(lazy="joined", cascade="all, delete")

    # reviews: Mapped[List['Review']] = relationship("Review", cascade="all, delete-orphan")

    def set_properties(self, properties: dict) -> None:
        for key, value in properties.get("attributes").items():

            # also append the tracklist / genre / subgenre if exists
            if key == "Model.Vinyl.Track.Track":
                for track in value:
                    self.tracks.append(generate_classinstance(key, track))
                continue

            if key == "Model.Vinyl.Associations.AscGenre":
                for genre in value:
                    self.genres.append(generate_classinstance(key, genre))
                continue

            if key == "Model.Vinyl.Associations.AscSubGenre":
                for sub_genre in value:
                    self.sub_genres.append(generate_classinstance(key, sub_genre))
                continue

            if key == "Model.Vinyl.Associations.AscSellerRecord":
                for seller in value:
                    self.seller.append(generate_classinstance(key, seller))
                    print(self.seller)
                continue

            setattr(self, key, value)

    def add_track(self, track: Track) -> None:
        """
        Add a new track to the list

        :param track: [Track]
        :return: None
        """
        self.tracks.append(track)

    def to_dict(self) -> dict:
        # Since we want the relationships converted to a dict too, ignore them at first and add them separately
        # otherwise they would be added as Class object list
        ret = dict((f.name, getattr(self, f.name)) for f in fields(self) if f.name not in ['tracks', 'sub_genres', 'genres'])
        ret['tracks'] = [track.to_dict() for track in self.tracks]
        ret['genres'] = [track.to_dict() for track in self.genres]
        ret['sub_genres'] = [track.to_dict() for track in self.sub_genres]
        return ret
