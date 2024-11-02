import Papa from 'papaparse';
import { base } from '$app/paths';

export async function load({ fetch, params }) {

  const responseCSV = await fetch(base + '/typical_smartphone_usage.csv', {headers: {'Content-Type': 'text/csv'}})
  let textCSV = await responseCSV.text()
  let parsedCSV = Papa.parse(textCSV, {header: true})

  return { 
    phoneCSV: parsedCSV.data 
  }
}