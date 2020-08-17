import React, { Component } from 'react';
import './App.css';
import Movie from './Movie';

class App extends Component {

  state = {}

componentDidMount(){
  // 외부 라이브러리 연동: D3, masonry, etc
  // 컴포넌트에서 필요한 데이터 요청: Ajax, GraphQL, etc
  // DOM 에 관련된 작업: 스크롤 설정, 크기 읽어오기 등
  this.__getMovies();

}

// ...this.state.movies 이전 영화리스트는 그대로 남기고 새롭게 추가
/*Loading States*/
__renderMovies = () => {
  const movies = this.state.movies.map((movie, index) => {
    return <Movie
     title={movie.title_english}
     poster={movie.medium_cover_image}
     key={movie.id}
     genres={movie.genres}
     synopsis={movie.synopsis} />
  })
  return movies
}

//비동기화 async 순서에상관없이 작업진행
__getMovies = async () => {
  const movies = await this.__callApi()
  //call api작업완료후에! (성공여부x) 리턴값을 movies에 set한다
  this.setState({
    movies
  })
}

__callApi = () => {
  //fetch를 이용해 url 불러오기 AJAX(url을 자바스크립트로 비동기화방법으로 불러온다.)
  return fetch('https://yts.mx/api/v2/list_movies.json?sort_by=download_count')
  .then(reponse => reponse.json())
  .then(json => json.data.movies)
  .catch(err => console.log(err))
}

  render() {
    const { movies } =this.state;
    return (
      <div className={movies ? "App": "App--loading"}>
        {movies ? this.__renderMovies() : 'Loading'}
      </div>
    );
  }
}

export default App;
