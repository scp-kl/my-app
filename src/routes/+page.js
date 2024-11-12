import Papa from 'papaparse';
import { base } from '$app/paths';

export async function load({ fetch, params }) {

  const responseCSV = await fetch(base + '/typical_smartphone_usage.csv', {headers: {'Content-Type': 'text/csv'}})
  let textCSV = await responseCSV.text()
  let parsedCSV = Papa.parse(textCSV, {header: true})


  const oCSV = await fetch(base + '/dataset_olympics.csv', {headers: {'Content-Type': 'text/csv'}})
  let otextCSV = await oCSV.text()
  let oparsedCSV = Papa.parse(otextCSV, {header: true})

  return { 
    phoneCSV: parsedCSV.data,
    olymCSV: oparsedCSV.data
  }
}