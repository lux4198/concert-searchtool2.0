import '../styles/globals.css'
import '../styles/index.css'

import { Roboto } from '@next/font/google'

// If loading a variable font, you don't need to specify the font weight
const roboto = Roboto({ subsets: ['latin'], weight : ['400', '500', '700'] })

export default function App({ Component, pageProps }) {
  return (
  <main className= {roboto.className}>
    <Component {...pageProps} />
  </main>)
}
