import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './feedback.component.html',
  styleUrl: './feedback.component.css'
})
export class FeedbackComponent {
  summary = '';
  rating = 0;
  tempRating = 0;
  comments = '';
  isSubmitted = false;
  submissionSuccess = false;

  constructor(private apiService: ApiService, private router: Router) { 
    const navigation = this.router.getCurrentNavigation();
    const state = navigation?.extras.state as { summary: string };
    if (state && state .summary) {
      this.summary = state.summary;
    }
   }

   setRating(rating: number){
    this.rating = rating;
   }

   setTempRating(rating: number) {
    this.tempRating = rating;
   }

  onSubmit() {
    this.apiService.submitFeedback(this.summary, this.rating, this.comments).subscribe(
      (response: any) => {
        this.isSubmitted = true;
        this.submissionSuccess = true;
      },
      (error) => {
        console.error('Error submitting feedback:', error);
        this.isSubmitted = true;
        this.submissionSuccess = false;
      }
    );
  }

  goBack() {
    window.history.back();
  }
}
