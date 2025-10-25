import { Routes } from '@angular/router';
import { SummarizeComponent } from './summarize/summarize.component';
import { FeedbackComponent } from './feedback/feedback.component';

export const routes: Routes = [
  { path: '', redirectTo: '/summarize', pathMatch: 'full' },
  { path: 'summarize', component: SummarizeComponent },
  { path: 'feedback', component: FeedbackComponent }
];

export class AppRoutes { }