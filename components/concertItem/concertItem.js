import Image from 'next/image';


import styles from './concertItem.module.css'
import Pic from '../../public/concertItemPic.png'


import moment from 'moment'
import 'moment/locale/de'
moment.locale('de')


export default function ConcertItem(props){

  const concert = props.concert
  const composers = concert.composers

  let formattedDate = moment(concert.date).format('DD. MMM YYYY')
  let formattedWeekday = moment(concert.date).format('dddd')
  // let formattedTime = moment(concert.date).format('HH:mm')

  return(
      <div className = {styles.card} >

        <div id = 'topside' className = {styles.card_top}>
            <div className = {styles.city_date}>
              <p>
                {concert.city}
              </p>
              <div className = {styles.date_picture}>
                  <p style = {{'fontWeight' : 'bold', 'marginTop': 'auto', 'marginRight': '1rem', }}>
                    {`${formattedWeekday} - ${formattedDate}`}
                  </p>
                  <Image src = {Pic} alt = 'pic' className= {styles.picture} width = '150' height= '150'/>
              </div>
            </div>
          <div id = 'ensemble_and_artists' className = {styles.rightside}>
            <a target={'_blank'} rel="noreferrer"  href={concert.link}>
              <p id = {'ensemble'} className = {styles.title}> {concert.title} </p>
            </a>
            <div id = 'musicians' className = {styles.musicians}>
                <table>
                  <tbody>
                    <tr>
                      <td style = {{'whiteSpace': 'nowrap'}}>
                        <p style = {{'fontWeight' : 'bold'}}>
                          {concert.conductor}
                        </p>
                      </td>
                      <td>
                        <p> {concert.conductor === '' ? '':'Dirigent'}</p>
                      </td>
                    </tr>
                    {Object.keys(concert.musicians).map((musician) =>
                        {return(
                          <tr key = {musician + concert.index}>
                            <td style = {{'whiteSpace': 'nowrap'}}>
                              <p style = {{'fontWeight' : 'bold'}}> {musician} </p>
                            </td>
                            <td >
                              <p> {concert.musicians[musician]}</p>
                            </td>
                          </tr>
                        )}
                        )}
                  </tbody>
                </table>
              </div>
            <div id = 'bottomside' className = {styles.card_bottom}>
                  <div id = 'composerWrap' className = {styles.composerWrap}>
                    <div className = 'composerExpand'>
                      <p>{`Werke von ${[...new Set(concert.composers)].join(', ')}`}</p>
                    </div>
                      <table className = {styles.block}>
                        {composers.map(
                          (composer, index) =>
                          concert.pieces[index].map(
                            (piece, pieceIndex) =>
                              <tbody>
                                <tr key = {piece + pieceIndex + concert.index}>
                                  <td style = {{'whiteSpace' : 'break-spaces', 'paddingBottom' : '3px' }}>
                                    <p style = {{'fontWeight' : 'bold',}}>
                                      {pieceIndex > 0 ? '' : composer}
                                    </p>
                                  </td>
                                </tr>
                                <tr >
                                  <td>
                                    <p  style = {{'fontStyle' : 'italic', 'textAlign' : 'center'}}>
                                      {piece}
                                    </p>
                                  </td>
                                </tr>
                              </tbody>
                          )
                        )}
                        {
                          concert.composers.length === 0 &&
                            <td> {concert.pieces} </td>
                        }
                      </table>
                  </div>
            </div>
          </div>
        </div>
      </div>
  )
}
