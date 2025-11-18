import { Component } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { UserService } from '../services/user.service';
import { Utils } from './utils';
import { MessageModel } from '../models/message.model';
import { RasaService } from '../services/rasa.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected year = new Date().getFullYear()
  protected waitingForResponse: boolean = false
  protected botThinkingPlaceholder: string = 'Thinking ...'
  protected isChatVisible: boolean = false
  protected userMessage: string = ''
  protected messages: MessageModel[] = []

  constructor(private router: Router, private utils: Utils) {
    this.messages.push({
      type: 'bot',
      text: 'How can I help you?'
    })
  }

  toggleChat() {
    this.isChatVisible = !this.isChatVisible
  }

  sendUserMessage() {
    if (this.waitingForResponse) return

    const trimmedMessage = this.userMessage.trim()
    this.userMessage = ''

    this.messages.push({
      type: 'user',
      text: trimmedMessage
    })
    this.messages.push({
      type: 'bot',
      text: this.botThinkingPlaceholder
    })

    RasaService.sendMessage(trimmedMessage)
      .then(rsp => {
        if (rsp.data.length == 0) {
          this.messages.push({
            type: 'bot',
            text: "Sorry, I didn't understand your question!"
          })
          return
        }

        for (let message of rsp.data) {
          this.messages.push({
            type: 'bot',
            text: message.text
          })
        }

        // TODO: Nedostaje uklanjne bot placeholder porike nakon sto se dobije odgovor!
      })


  }

  getUserName() {
    const user = UserService.getActiveUser()
    return `${user.firstName} ${user.lastName}`
  }

  hasAuth() {
    return UserService.hasAuth()
  }

  doLogout() {
    this.utils.showDialog(
      "Are you sure you want to logout?", () => {
        UserService.logout()
        this.router.navigateByUrl('/login')
      },
      "Logout Now",
      "Don't Logout"
    )
  }
}
