import pytest
from project.dao import MoviesDAO
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="movie", description="description", trailer="trailer", year=1, rating=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="movie_1", description="description_1", trailer="trailer_1", year=2, rating=2)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1, movies_dao):
        """
        Checks if the function returns a proper movie object from the database.
        """
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        """
        Checks if the function returns a 404 when the requested
        movie object does not exist in the database.
        """
        assert not movies_dao.get_by_id(3)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        """
        Checks if the function returns a proper list of movie objects from the database.
        """
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        """
        Checks if the pagination works correctly with a
        list of movie objects from the database.
        """
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []
