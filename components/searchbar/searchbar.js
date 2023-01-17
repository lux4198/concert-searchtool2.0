import { useState } from 'react'
import styles from './searchbar.module.css'


function getPlaceholder(query, concerts){
    if(!query){
        return ''
    }
    else{
        let placeholder = concerts.find(concert => concert.conductor.startsWith(query))
        return placeholder? placeholder.conductor : ''
    }
        
}


export default function Searchbar(props) {
    const concerts = props.concerts

    const [input, setInput] = useState('')


    return (
        <div className= {styles.searchbarContainer}>
            <div className= {styles.complete}>{getPlaceholder(input, concerts)}</div>
             <form onSubmit={evt => {evt.preventDefault(); props.onSubmit(evt.target[0].value)}}>
                 <input value = {input} onChange = {(evt) => setInput(evt.target.value)} type="text" placeholder= {'Search ...'} className= {styles.searchbar} id = 'searchInput'>
                 </input>
             </form>
        </div>
    )
}
