import axios from 'axios'

const base = 'https://template.com'

export async function getTasks() {
  return (
    await axios.get(`https://opportunity-cup-2021.herokuapp.com/data`)
  ).data.data
}

export async function setOffset(id: number, offset: number) {
  return (
    await axios.get(`https://opportunity-cup-2021.herokuapp.com/offset`, {
      params: {
        id: id,
        offset: offset
      }
    })
  ).data
}
