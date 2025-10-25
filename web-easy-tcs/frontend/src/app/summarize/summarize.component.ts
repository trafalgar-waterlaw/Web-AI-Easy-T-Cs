import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-summarize',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './summarize.component.html',
  styleUrl: './summarize.component.css'
})
export class SummarizeComponent {
  text = '';
  summary = '';
  isLoading = false;
  showSummary = false;

  constructor(private apiService: ApiService, private router: Router) { }

  onSubmit() {
    this.isLoading = true;
    this.apiService.summarizeText(this.text).subscribe(
      (response: any) => {
        this.summary = response.summary;
        this.isLoading = false;
        this.showSummary = true;
      },
      (error) => {
        console.error('Error summarixing text:', error);
        this.isLoading = false
      }
    );
  }

  goToFeedback() {
    this.router.navigate(['/feedback'], { state: { summary: this.summary }});
  }
}
