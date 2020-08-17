import React from 'react';
import PropTypes from 'prop-types';
import LinesEllipsis from 'react-lines-ellipsis'
import './Movie.css';

/* 클래스 컴포넌트
class Movie extends Component{

    static propTypes = {
        title: PropTypes.string.isRequired,
        poster: PropTypes.string.isRequired
    }

    render(){
        return (
            <div>
                <MoviePoster poster={this.props.poster}/> 
                <h1>{this.props.title}</h1>
            </div>
        )
    }
}

class MoviePoster extends Component{

    static propTypes = {
        poster: PropTypes.string.isRequired
    }
    
    render(){
        return (
            <img src={this.props.poster}/>
        )
    }
}
*/

/*함수 컴포넌트*/
function Movie({title,poster,genres,synopsis}){
    return(
        <div className="Movie">
            <div className="Movie_Columns">
                <MoviePoster poster={poster} alt={title} />
            </div>
            <div className="Movie_Columns"> 
                <h1>{title}</h1>
                <div className="Movie__Genres">
                    {genres.map((genre, index) => <MovieGenre genre={genre} key={index}/>)}
                </div>
                <div className="Movie__Synopsis">
                <LinesEllipsis
                    text={synopsis}
                    maxLine='3'
                    ellipsis='...'
                    trimRight
                    basedOn='letters'
                />
                </div>
            </div>
        </div>
    )
}
/*genre는 여러개일수있기때문에 array로 맵핑 해준다. */


function MoviePoster({poster, alt}){
    return (
        <img src={poster} alt={alt} title={alt} className="Movie__Poster" />
    )
}

function MovieGenre({genre}){
    return (
        <span className="Movie__Genre">{genre}</span>
    )
}

/*proptype*/
Movie.proptype = {
    title: PropTypes.string.isRequired,
    poster: PropTypes.string.isRequired,
    genres: PropTypes.array.isRequired,
    synopsis: PropTypes.string.isRequired
}

MoviePoster.proptype = {
    poster: PropTypes.string.isRequired,
    alt: PropTypes.string.isRequired
}

MovieGenre.proptype = {
    genre: PropTypes.string.isRequired
}


export default Movie
