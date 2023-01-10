import supabase from "../utils/supabase/supabase"
import ConcertItem from "../components/concertItem/concertItem"


export default function Home({concerts}) {
  
  // console.log({concerts})

  return (

    <div class = 'concert-item-container'>
      {concerts.map((concert) => 
        <ConcertItem concert = {concert} /> 
      )}
    </div>
  )
}


export const getStaticProps = async () => {
  const { data: concerts } = await supabase.from('concerts').select()

  return {
    props: {
      concerts,
    },
  };

}
