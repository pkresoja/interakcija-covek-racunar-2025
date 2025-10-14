import axios from "axios";
import { MovieModel } from "../models/movie.model";

const client = axios.create({
    baseURL: 'https://movie.pequla.com/api',
    headers: {
        'Accept': 'application/json',
        'X-Name': 'ICR/2025'
    }
})

export class MovieService {
    static async getMovies(search: string = '') {
        return client.get<MovieModel[]>(`/movie?search=${search}`)
    }

    static async getMovieByPermalink(permalink: string) {
        return client.get<MovieModel>(`/movie/short/${permalink}`)
    }
}