import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  summarizeText(text: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/summarize`, {text});
  }

  submitFeedback(summary: string, rating: number, comments: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/feedback`, { summary, rating, comments});
  }
}
