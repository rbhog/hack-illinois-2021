require('dotenv').config()
const axios = require('axios')
const datepicker = require('js-datepicker')

let wantedDate = new Date()

const picker = datepicker('#simple', {
    onSelect: (instance, date) => {
        wantedDate = date
        console.log(date)
    },
    dateSelected: wantedDate,
})

mapboxgl.accessToken = process.env.MAPBOX_TOKEN

var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-88.2249588460582, 40.113983290286015],
  zoom: 17
})

console.log("map created")


