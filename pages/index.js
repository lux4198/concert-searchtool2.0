import supabase from "../utils/supabase/supabase"
import ConcertItem from "../components/concertItem/concertItem"
import Searchbar from "../components/searchbar/searchbar";

import { useState } from "react";
import Fuse from "fuse.js";

// returns current date in 2 formats
const getCurrentDate = () => {
  let today = new Date(); 
  let dd = String(today.getDate()).padStart(2, '0'); 
  let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0 
  let yyyy = today.getFullYear() ; 
  today = mm + '-' + dd + '-' + yyyy; 
  const today2 = yyyy + '-' + mm + '-' + dd; 

  return [today, today2]; 
}


export const getStaticProps = async () => {

// get current date 
const today = getCurrentDate()[0]; 

// get future concerts
  const { data: allConcerts } = await supabase.from('concerts').select().gte('datetime', today).order('datetime')

  return {
    props: {
      allConcerts,
    },
  };
}


// search allConcerts array recursively with fuse.js
function searchConcerts(query, index, allConcerts){
  // spaces in query are ignored 
  if(!query[index]){
    return allConcerts
  }

  // extended search needed to search for exact match ('${query[index]})
   const options = {
    useExtendedSearch : true, 
    keys : [['title'], ['conductor'], ['pieces'], ['composers'], ['musicians'], ['city']]
  }

  const searcher = new Fuse(allConcerts, options);
  // filter search results for each search item
  const queryResult = searcher.search(`'${query[index]}`).map(result => result.item)
  
  if(index == query.length - 1){
    return queryResult
  } else {
    return searchConcerts(query, index += 1, queryResult)
  }
}


export default function Home({allConcerts}) {

  // state tracks how many concerts are rendered at a time 
  const [concertIndex, setConcertIndex] = useState(20)
  
  // state for query from searchbar
  const [query, setQuery] = useState('')

  // tracks if filter items are visible
  const [filterVisibility, setFilterVisibility] = useState(false)

  // tracks filter date
  const [filterDate, setFilterDate] = useState(getCurrentDate()[1])

  const cities = ['Berlin', 'Hamburg', 'Frankfurt', 'München', 'Dresden']
  
  // tracks which cities are active in city filter 
  const [cityState, setCityState] = useState(new Array(5).fill(false))

  const updateCityState = (index) => {
    let newArr = [...cityState]
    newArr[index] = !newArr[index]
    setCityState(newArr)
  }

  const filterCities = (concerts) => {
    // filter cities that have true entry for their index in cityState
    const filteredCities = cities.filter((city, index) => {if(cityState[index]){ return city }})
    
    if(filteredCities.length == 0){
      return concerts
    }
    const filteredConcerts = concerts.filter(concert => filteredCities.includes(concert.city))
    return filteredConcerts
  }

  // filters for concerts in the future of selected date 
  const filterForDate = (concerts) => {
    const queryDate= new Date(filterDate)

    return concerts.filter((concert) => { 
      const concertDate = new Date(concert.datetime)

      if(concertDate.getTime() > queryDate.getTime()){
        return concert
      }
     })
  }

  // filter function combines city and date filter 
  const filterConcerts = (concerts) => {
    const concertCities = filterCities(concerts)
    return filterForDate(concertCities)
  }

  // if query is empty return allConcerts, else search for query
  const concerts = (!query[0])? filterConcerts(allConcerts) : searchConcerts(query, 0, filterConcerts(allConcerts))

  // console.log(concerts)

  const onSubmit = (query) => {
    setQuery(query.split(" "))
  }

  return (
    <div>
      <div class = 'home-page-container'>

        <div class = 'title-search-container'>
          <h1>Wer Spielt Franz Liztz?</h1>
          <p>Suche aus über 1000 klassischen Konzerten in ganz Deutschland.</p>
          <Searchbar input = {query} onSubmit = {(evt) => onSubmit(evt)}  concerts = {concerts}/>
          <div class = 'search-filter-container'>
            <div class = 'datepicker'>
              <input type= 'date' value = {filterDate} onChange = {(e) => setFilterDate(e.target.value)}/>
            </div>
            <div class = 'drop-down-element'>
              <div onClick = {() => setFilterVisibility(!filterVisibility)} class = 'drop-down-title'>
                <span style = {{'letterSpacing' : '0.1ch'}}>Stadt</span>
                <img class = {filterVisibility? 'arrow-down active' : 'arrow-down'} src= {'svg/arrowDown.svg'} alt = 'arrowDown' height={'10px'} width = {'15px'}/>
              </div>
              <ul class = {filterVisibility? 'filter-items-list visible' : 'filter-items-list'} >
                {cities.map((city, index) => 
                  <li onClick = {() => updateCityState(index)} class = {cityState[index]? 'filter-item active' : 'filter-item'}>{city}</li>)}
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class = 'concert-item-container'>
        {concerts.slice(0, concertIndex).map((concert) =>
          <ConcertItem concert = {concert} />
        )}
        <button class = 'extend-concerts-button' onClick = {() => setConcertIndex(concertIndex + 20)}>
          <img src= {'svg/arrowDown.svg'} alt = 'arrowDown' height={'15px'} width = {'20px'}/>
        </button> 
      </div>
    </div>
  )
}


