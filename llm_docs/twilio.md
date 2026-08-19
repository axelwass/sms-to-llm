---
"@context": https://schema.org
"@type": TechArticle
"@id": https://www.twilio.com/docs/usage/webhooks#article
headline: Introduction to Webhooks
description: Launching point for information about Twilio webhooks, including product-specific guides, tutorials, and getting started information.
url: https://www.twilio.com/docs/usage/webhooks
inLanguage: en
dateModified: 2026-08-13T17:02:08.000Z
author:
  "@type": Organization
  name: Twilio Developer Education Team
publisher:
  "@type": Organization
  name: Twilio
---

# Introduction to Webhooks

Webhooks are user-defined [HTTP][] callbacks. They trigger when an event occurs in a web application and can help integrate different applications or third-party APIs, such as Twilio.

Twilio uses webhooks to notify your application when events occur, such as receiving an SMS message or getting an incoming phone call. When an event occurs, Twilio makes an HTTP `POST` or `GET` request to the URL you configured for the webhook. The Twilio request includes details of the event, such as the incoming phone number or the body of an incoming message. Many other modern web services like GitHub and Slack also make use of webhooks to communicate events.

![SMS webhook request cycle from sender to Twilio to recipient.](https://docs-resources.prod.twilio.com/79151a29480b443e107245a4c278fddeee9a1f654e2eaf1c57af02ba00a9d971.gif)

Some webhooks provide information. For example, they can notify you when a voice-call recording is ready for download. Others require your web application to respond—for example, to tell Twilio what to do when someone calls your Twilio phone number.

## Get started with webhooks

Watch the following Twilio Tip video, and read the [Getting started with Twilio webhooks guide][].

https://www.youtube.com/watch?v=aLjSNfoJCYc

## Webhooks by product

Each Twilio product uses webhooks differently. To learn more about which webhooks each product uses and how to set them up with your application, visit these pages:

* [Voice][]
* [Messaging][]
* [Conversations][]
* [Sync][]

## Twilio runtime webhooks

Webhooks aren't just limited to products. When events occur in your application, you can also have Twilio send you webhooks. These events include billing levels reaching a threshold or errors that occur when Twilio calls your web application. You can set up a pipeline that sends your webhooks to Slack, Microsoft Teams, or another chat system. You can also set up a webhook that notifies you by email.

Learn more about each of these areas on these pages:

* [Debugging Events Webhook][]
* [REST API: Usage Triggers][]

## What's next?

For an in-depth discussion of webhooks, guidance on validating that inbound webhooks originate from Twilio, and answers to common questions, see:

* [Overview of Webhooks, Callbacks, and Inbound Requests][]
* [Webhook Security][]
* [Webhooks FAQ][]

## Webhook tutorials

To implement webhooks and explore their capabilities, follow these tutorials:

* [Track Delivery Status of Messages][]
* [Receive and Reply to SMS and MMS Messages][]
* [Serverless Webhooks with Azure Functions and C#][]
* [Serverless Webhooks with Azure Functions and Node.js][]
* [Creating an ASP.NET MVC Webhook Project][]

[Conversations]: /docs/conversations-classic/conversations-webhooks

[Creating an ASP.NET MVC Webhook Project]: /docs/usage/tutorials/how-to-set-up-your-csharp-and-asp-net-mvc-development-environment

[Debugging Events Webhook]: /docs/usage/troubleshooting/debugging-event-webhooks

[Getting started with Twilio webhooks guide]: /docs/usage/webhooks/getting-started-twilio-webhooks

[HTTP]: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol

[Messaging]: /docs/usage/webhooks/messaging-webhooks

[Overview of Webhooks, Callbacks, and Inbound Requests]: /docs/usage/webhooks/webhooks-overview

[REST API: Usage Triggers]: /docs/usage/api/usage-trigger

[Receive and Reply to SMS and MMS Messages]: /docs/messaging/tutorials/how-to-receive-and-reply

[Serverless Webhooks with Azure Functions and C#]: /docs/usage/tutorials/serverless-webhooks-azure-functions-and-csharp

[Serverless Webhooks with Azure Functions and Node.js]: /docs/usage/tutorials/serverless-webhooks-azure-functions-and-node-js

[Sync]: /docs/sync/webhooks

[Track Delivery Status of Messages]: /docs/messaging/guides/track-outbound-message-status

[Voice]: /docs/usage/webhooks/voice-webhooks

[Webhook Security]: /docs/usage/webhooks/webhooks-security

[Webhooks FAQ]: /docs/usage/webhooks/webhooks-faq
