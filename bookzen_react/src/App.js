import React, { Component } from 'react';
import './App.css';

const DEFAULT_QUERY = '';
const DEFAULT_PAGE = 1
const DEFAULT_HPP = '12'

const PATH_BASE = 'http://bookzen.top/bookzen/api/v1.0';
const PATH_SEARCH = '/books';
const PARAM_SEARCH = 'keyword=';
const PARAM_PAGE = 'page='
const PARAM_HPP = 'per_page='

class App extends Component {
  constructor(props){
    super(props)

    this.state = {
      data: {},
      results: {},
      searchTerm: DEFAULT_QUERY,
      searchKey: '',
    }

    this.needToSearchBooks = this.needToSearchBooks.bind(this)
    this.setSearchBooks = this.setSearchBooks.bind(this);
    this.fetchSearchBooks = this.fetchSearchBooks.bind(this);
    this.onSearchChange = this.onSearchChange.bind(this);
    this.onSearchSubmit = this.onSearchSubmit.bind(this);
    // this.onSort = this.onSort.bind(this)
  }

  needToSearchBooks(searchTerm) {
    return !this.state.results[searchTerm]
  }

  setSearchBooks(result) {
    const { books, page } = result
    const { searchKey, results } = this.state

    const oldBooks = results && results[searchKey]
      ? results[searchKey].books
      : []

    const updatedBooks = [
      ...oldBooks,
      ...books
    ]

    this.setState({ results: { ...results, [searchKey]: { books: updatedBooks, page }}, data: result })
  }

  fetchSearchBooks(searchTerm, page){
      fetch(`${PATH_BASE}${PATH_SEARCH}?${PARAM_SEARCH}${searchTerm}&${PARAM_PAGE}${page}&${PARAM_HPP}${DEFAULT_HPP}`)
      .then(response => response.json())
      .then(result => this.setSearchBooks(result))
  }

  componentDidMount() {
      const { searchTerm } = this.state
      this.setState({ searchKey: searchTerm})
      this.fetchSearchBooks(searchTerm, DEFAULT_PAGE)
  }

  onSearchChange(event) {
      this.setState({searchTerm: event.target.value})
  }

  onSearchSubmit(event) {
    const { searchTerm } = this.state
    this.setState({ searchKey: searchTerm })
    if (this.needToSearchBooks(searchTerm)) {
      this.fetchSearchBooks(searchTerm, DEFAULT_PAGE)
    }
    event.preventDefault()
  }

  render() {
    const { searchTerm, results, searchKey, data } = this.state
    const page = (results && results[searchKey] && results[searchKey].page) || 0
    const list = (results && results[searchKey] && results[searchKey].books) || []
    console.log(results)
    return (
      <div key={ results.id } className="App">
        <NavBar />
        { searchTerm === '' && Object.getOwnPropertyNames(results).length === 0
          ? <Index
            value={searchTerm}
            onSubmit={this.onSearchSubmit}
            onChange={this.onSearchChange}
            >
            Search
            </Index>
          : <Search
            value={searchTerm}
            onSubmit={this.onSearchSubmit}
            onChange={this.onSearchChange}
            >
            Search
            </Search>
          }
        <div className="columns">
            <div className="column is-12"></div>
        </div>
        <BookList list={ list } />
          <div className="columns">
              <div className="column is-12"></div>
          </div>
        { results[searchKey]
        ? <Pagination
            list={ data }
            onClickNext={() => this.fetchSearchBooks(searchTerm, page + 1)}
          />
        : null
        }
          <div className="columns">
              <div className="column is-12"></div>
          </div>
      </div>
    );
  }
}

const Index = ({ onSubmit, value, onChange, children }) => {
  return (
    <section className="hero is-large">
      <div className="hero-body">
        <Search
          value={value}
          onSubmit={onSubmit}
          onChange={onChange}
          >
          Search
        </Search>
      </div>
    </section>
  )
}

const Pagination = ({ list, onClickNext }) => {
  return (
    <div className="container has-text-centered">
      <div className="columns">
      <div className="column is-2-desktop is-offset-5-desktop is-8-mobile is-offset-2-mobile">
        <a
          className={"button " + (!list.next ? " is-disabled" : " is-focused")}
          onClick={onClickNext}
          >
          Xem thêm
        </a>
      </div>
    </div>
  </div>
  )
}

const BookList = ({ list }) => {
  return (
    <div className="container has-text-centered">
        <div className="columns is-multiline">
        { list.map( book =>
            <div key={book.id} className="column is-2 is-8-mobile is-offset-2-mobile">
                <div className="card">
                  <div className="card-image">
                      <a href={book.url} rel="nofollow" target="_blank">
                        <figure className="image is-square">
                            <img src={ book.image_uri } alt="" />
                        </figure>
                    </a>
                  </div>
                  <div className="card-content">
                    <div className="media">
                      <div className="media-content">
                          <a href={ book.url } rel="nofollow" target="_blank">
                              <p className="title is-5">{ book.name }</p>
                          </a>
                          <p className="subtitle is-6">{ book.website } - { book.price }</p>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
          )
        }
        </div>
    </div>
  )
}


const Search = ({ onSubmit, value, onChange, children }) => {
  return (
    <div className="container has-text-centered">
        <h1 className="title">
            Bookzen
        </h1>
        <h2 className="subtitle">
            Tìm giá tốt nhất cho cuốn sách ưa thích của bạn
        </h2>
        <form onSubmit={onSubmit} className="control">
            <div className="columns is-mobile">
                <div className="column is-10-mobile is-offset-1-mobile is-8-desktop is-offset-2-desktop">
                    <input
                      placeholder="Tên sách, tên tác giả, từ khóa v.v..."
                      className="input is-primary is-medium"
                      type="text"
                      value={value}
                      onChange={onChange}
                      autoFocus={true}
                    />
                </div>
            </div>
            <div className="columns is-mobile">
                <div className="column is-2-desktop is-offset-5-desktop has-text-centered">
                    <button type="submit" className="button is-primary is-medium">{children}</button>
                </div>
            </div>
        </form>
    </div>
  )
}


const NavBar = () => {
  function toggleNav() {
      var nav = document.getElementById("nav-menu");
      var className = nav.getAttribute("class");
      if(className === "nav-right nav-menu") {
          nav.className = "nav-right nav-menu is-active";
      } else {
          nav.className = "nav-right nav-menu";
      }
  }
  return (
        <nav className="nav">
            <div className="container">
                <div className="nav-left">
                    <a className="nav-item is-brand" href="">
                        <h1 className="title is-3">BOOKZEN</h1>
                    </a>
                </div>

                <div className="nav-center">
                    <a className="nav-item" href="https://github.com/tudoanh/bookzen">
                        <span className="icon">
                            <i className="fa fa-github" />
                        </span>
                    </a>
                    <a className="nav-item" href="#">
                        <span className="icon">
                            <i className="fa fa-instagram" />
                        </span>
                    </a>
                </div>

                <span id="nav-toggle" className="nav-toggle" onClick={toggleNav} >
                    <span></span>
                    <span></span>
                    <span></span>
                </span>

                <div id="nav-menu" className="nav-right nav-menu">
                    <a className="nav-item" href="https://medium.com/@doanhtu">
                        /blog
                    </a>
                    <a className="nav-item" href="">
                        /contact
                    </a>
                </div>
            </div>
          </nav>
  )
}

export default App;
