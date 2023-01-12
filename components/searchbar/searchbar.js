import { useState } from 'react'
import styles from './searchbar.module.css'


function getPlaceholder(query, concerts){
    if(!query){
        return ''
    }
    else{
        let placeholder = concerts.find(concert => concert.title.startsWith(query))
        return placeholder? placeholder.title : ''
    }
        
}



export default function Searchbar(props) {
    const concerts = props.concerts

    const [input, setInput] = useState('')

    return (
        <div className= {styles.searchbarContainer}>
            <div className= {styles.complete}>{getPlaceholder(input, concerts)}</div>
             <input value = {input} onChange = {e => setInput(e.target.value)} type="text" placeholder= {'Search ...'} className= {styles.searchbar} id = 'searchInput'>
             </input>
        </div>
    )
}
