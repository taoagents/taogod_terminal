from taogod_terminal.adapters.github.base_adapter import BaseGithubAdapter

nineteen_roadmap = """
# **👀 nineteen [τ, τ] SN19**
Giving access to Bittensor with Decentralized subnet inference at scale.

# Subnet 19 👀
Subnet 19 is decentralised inference of AI models. We call ourselves `Nineteen 👀`. Bittensor has the Nineteen of being the most powerful force in AI, powering the world through decentralisation. SN19 is all about fulfilling that `Nineteen` by getting decentralised AI into the hands of all.

We have a focus on inference, currently offering access to the best open source LLM's, Image generation models (including those trained on datasets from subnet 19), and other miscellaneous models such as embedding models. We've even home grown and open sourced our own workflows, such as avatar generation.

# Decentralisation
Nothing is more important than decentralisation - we must be decentralised. We rely on no centralised API's - the miners' and validators' all run their own models. No single provider can bring us down.

## Decentralised miners
Miners all run open source models on any hardware they choose. They're incentivised by three things:
- Volume (amount of tokens, for example)
- Speed of requests (Measured in Tokens/s, for example)
- Quality of requests (Measured by accuracy compared to base model)

They're incentivised over a range of tasks, independently of each other. Miners have the option of choosing which tasks they want to run, and the volume they want to run for each. The more volume they have, the more rewards they get!

## Decentralised Validators
Validators operate as decentralised access points to the network. In a one-click fashion, Validators can offer up their miner access to the world, with a clear path to monetisation. 

They check and score the miners through 'Checking servers' that they run themselves on their own hardware. No centralisation to be found here.

## Organic scoring is a primary citizen
All organic requests can be scored, and checked for the upmost quality. Not only that, but we always keep track of the miners who are most likely to be available to answer organic requests, meaning the lowest latency and highest reliability possible! The user experience is the most important thing about SN19 - allowing validators to monetise and the world to experience Bittensor.

# Deep dive into the subnet mechanism
The subnet is split into `tasks`. These `tasks` are things like:
- Llama3.1 70B text generation [1]
- Stable Diffusion text to image generation [2]

Each of these independent tasks have a weighting associated with them (say [1]: 60%, [2]: 40%, for example ). Note they sum to 100%!

First, miners configure their servers and associate a specific capacity or volume for the task. Validators then fetch the capacities that each miner can handle for that particular task. Every 60 minutes (this interval is configurable), validators perform several critical steps for each miner.

Validators begin by determining the percentage of the miner's capacity they will test. They estimate how many queries are needed during the scoring period to test this capacity accurately. These queries are sent at regular intervals, and validators keep track of the results for quality scoring. They carefully note any failed queries or instances where miners rate limit the validator.

At the end of the scoring period, validators calculate a ﻿period score for each miner. This score reflects the percentage of requests that were correctly responded to. Miners are penalized for missed queries based on the volume left unqueried. If the announced volume is fully utilized, no penalties are imposed. However, if a miner is queried only once or twice and fails to respond, the penalties are more severe.

Simultaneously, validators assess the quality of all responses from fiber.src.miners, maintaining a running tally of their 'quality scores' and 'speed factors' (rewarding both speed and correctness). When it is time to set weights, validators calculate a volume-weighted average period score for each miner. This score is then multiplied by the miner's combined quality score to derive an overall score for that specific task.

Finally, the overall scores for each miner are combined across all tasks - which is what makes the tasks completely optional for miners. The different scores for all tasks are then summed up to derive a final overall score for each miner, which is used to set weights appropriately.

Phew!

### Ok that's a lot of text, what does it mean?
It means a few things:
- Miners can run tasks completely optionally. The more tasks they run, with greater volumes and speeds, the more incentive they will get.
- By controlling the reward distribution to miners, we can directly incentivise greater volumes and speeds for tasks that get greater organic usage. We could even give power for validators to have a stake weighted 'vote' for the tasks they care about...
- We can add as many tasks as we like! If there's demand for something we can add it! If not, we can remove it! No registrations or deregistrations needed, miners can just scale up and scale down their capacity as needed.
- Miners have the ability to rate limit explicitly to validators without incurring a greater penalty. This means we can much more effectively load balance between miners, to make sure any organic requests can be always handled by a miner who is capable of performing that task!
- There's nothing special about a synthetic or organic query. No distinction can be made on the miner side, but validators can still give preferential treatment to organics!ß
"""

targon_roadmap = """
# Targon: A Deterministic Verification of Large Language Models

Targon (Bittensor Subnet 4) is a deterministic verification mechanism that is
used to incentivize miners to run openai compliant endpoints and serve synthetic
and organic queries.

> Example model config file `models.txt`
>
> ```
> NousResearch/Meta-Llama-3.1-8B-Instruct
> NousResearch/Meta-Llama-3.1-70B-Instruct
> NousResearch/Meta-Llama-3.1-405B-Instruct
> ```


### Targon Hub (WIP)

The goal of the hub is to give validators a simple way to directly generate
revenue off of their bittensor bandwidth. This is designed as a template for
validators to take and create their own branded hubs with, however pull requests
are still encouraged.

If you are interested in running your own instance of Targon Hub, you will need
to add an additional flag to save the records of miners' responses to a
PostgreSQL DB.

"""

pretraining_roadmap = """
# Introduction

Bittensor subnet 9 rewards miners for producing pretrained Foundation-Models on the Falcon Refined Web dataset. It acts like a continuous benchmark whereby miners are rewarded for attaining the best losses on randomly sampled pages of Falcon given a consistent model architecture. The reward mechanism works as follows:

    1. Miners train and periodically publish models to hugging face and commit the metadata for that model to the Bittensor chain.
    2. Validators download the models from hugging face for each miner based on the Bittensor chain metadata and continuously evaluate them, setting weights based on the performance of each model against the Falcon dataset. They also log results to [wandb](https://wandb.ai/opentensor-dev/pretraining-subnet).
    3. The Bittensor chain aggregates weights from all active validators using Yuma Consensus to determine the proportion of TAO emission rewarded to miners and validators. 

## Incentive Mechanism

Bittensor hosts multiple incentive mechanism through which miners are evaluated by validators for performing actions well. Validators perform the process of evaluation and 'set weights', which are transactions into Bittensor's blockchain. Each incentive mechanism in Bittensor is called a 'subnet' and has an identifier (This particular mechanism has subnet uid 9). Weights and the amount of TAO held by the validators become inputs to Bittensor's consensus mechanism called Yuma Consensus. YC drives validators towards a consensus, agreement about the value of the work done by miners. The miners with the highest agreed upon scores are minted TAO, the network digital currency.

Miners within this subnet are evaluated based on the number of times the model they have hosted has a lower loss than another model on the network when randomly sampling from the near infinite Falcon Refined Web pretraining dataset. To perform well, miners must attain the lowest loss on the largest number of random batches. Finding the best model and delta at the earliest block ensures the most incentive.
"""

apex_roadmap = """

# Introduction

This repo defines an incentive mechanism to create a distributed conversational AI for Subnet 1 (SN1).

Validators and miners are based on large language models (LLM). The validation process uses **internet-scale datasets and goal-driven behaviour to drive human-like conversations**.

# Agentic Tasks

Subnet one utilizes the concept of "Tasks" to control the behavior of miners. Validator create a variety of tasks, which include a "challenge" for the miner to solve, and sends them to 100 miners, scoring all the completions they send back. 

## Task Descriptions

### 1. **QA (Question Answering)**
The miner receives a question about a specific section from a Wikipedia page. The miner must then find the original context in the specified section and use it to return an accurate answer. References are generated using the validators privileged knowledge of the context, and miner complestions are scored based on similarity metrics.

### 2. **Summarization**
Similar to QA, but the miner uses the entire Wikipedia page instead of a specific section. The miner reads the whole page, summarizes it, and provides a concise answer.

### 3. **DateQA**
The miner receives a question about an event from Wikipedia. The miner must search through Wikipedia for the relevant event and return the correct answer based on the findings. References are again generated with validator's knowledge of the context, and similarity metrics are used to score miner completions. 

### 4. **Inference**
A question is given with some pre-seeded information and a random seed. The miner must perform an inference based on this information to provide the correct answer. Completions are scored based on similarity metrics.

### 5. **MultiChoice**
The miner is presented with a question from Wikipedia along with four possible answers (A, B, C, or D). The miner must search Wikipedia and return the correct answer by selecting one of the given options. Miner completions are scored by Regex matching. 

### 6. **Programming**
The miner receives a code snippet that is incomplete. The task is to complete the code snippet to perform its intended function. The validator generates a reference using it's internal LLM, and the miner is scored based on its similarity to this reference. 

### 7. **Web Retrieval**
The miner is given a question based on a random web page and must return a scraped website that contains the answer. This requires searching the web to locate the most accurate and reliable source to provide the answer. The miner is scored based on the embedding similarity between the answer it returns and the original website that the validator generated the reference from. 
"""

coldint_roadmap = """
Subnet creation changelog:
#3379782: register 5HHHHHzgLnYRvnKkHd45cRUDMHXTSwx7MjUzxBrKbY4JfZWn for SN29
Register coldint.io
Fork pretraining from https://github.com/macrocosm-os/pretraining
Create GitHub https://github.com/coldint
Create WandB https://wandb.ai/coldint
Create HuggingFace https://huggingface.co/coldint
Apply for Discord channel
Cleanup validator codebase
Implement scoring mechanism in validator
Change sample packing in model evaluation logic
Implement bug bounty, aka “Hall of Fame” reward mechanism
Spin up two validators and one miner
#3413001: publish subnet 29 metadata on-chain, release GitHub and website 🚀
TODO: immediate post-launch steps
Spread the word about SN29 renaming to actors not using on-chain identity data
(Suggest to those actors to use on-chain identity data…)
Implement competitions to allow training for specific goals
Clean up mining codebase and publish on GitHub
Analyze possibilities and implement on-chain announcement of validator startup with version information
Finalize testing with arbitrary tokenizer (immediately saves up to 800m of 6.9b parameters on reference model)
Launch first additional competition (weight fraction 0.1) with arbitrary tokenizer
Collect results and feedback on subnet and competition performance
2024 Q3
Consult with community and create a list of competitions, scheduled well in advance
Research model merging tactics to unlock distributed training potential of subnet
Draft shortlist of finetuning targets for niche models
Launch first additional competition for niche model
Publish model_surgeon.py, a commandline tool to modify models
2024 Q4
Strive to have 5 niche models in training
Provide boilerplate code for web applications, host apps showcasing top models
Research external benchmarks to assess subnet efficacy
2025 and beyond
Pretrain-as-a-Service: commercial opportunities
Finetune-as-a-Service: commercial opportunities
"""

dataverse_roadmap = """
# Introduction

Data is a critical pillar of AI and Data Universe is that pillar for Bittensor.

Data Universe is a Bittensor subnet for collecting and storing large amounts of data from across a wide-range of sources, for use by other Subnets. It was built from the ground-up with a focus on decentralization and scalability. There is no centralized entity that controls the data; the data is stored across all Miner's on the network and is queryable via the Validators. At launch, Data Universe is able to support up to 50 Petabytes of data across 200 miners, while only requiring ~10GB of storage on the Validator.

# Overview

The Data Universe documentation assumes you are familiar with basic Bittensor concepts: Miners, Validators, and incentives. If you need a primer, please check out https://docs.bittensor.com/learn/bittensor-building-blocks.

In the Data Universe, Miners scrape data from a defined set of sources, called DataSources. Each piece of data (e.g. a webpage, BTC prices), called a DataEntity, is stored in the miner's database. Each DataEntity belongs to exactly one DataEntityBucket, which is uniquely identified by its DataEntityBucketId, a tuple of: where the data came from (DataSource), when it was created (TimeBucket), and a classification of the data (DataLabel, e.g. a stock ticker symbol). The full set of DataEntityBuckets on a Miner is referred to as its MinerIndex.

Validators periodically query each Miner to fetch their latest MinerIndexes and store them in a local database. This gives the Validator a complete understanding of all data that's stored on the network, as well as which Miners to query for specific types of data. Validators also periodically verify the correctness of the data stored on Miners and reward Miners based on the amount of [valuable data](#data-value) the Miner has. Validators log to [wandb](https://wandb.ai/macrocosmos/data-universe-validators) anonymously by default.

Optionally, Miners upload their local stores to HuggingFace for public dataset access. This data is anonymized for privacy purposes to comply with the Terms of Service per each data source. See the [HuggingFace](docs/huggingface_setup.md) docs for more information on HuggingFace uploads. In the future, publicly uploading data to HuggingFace will be required.

See the [Miner](docs/miner.md) and [Validator](docs/validator.md) docs for more information about how they work, as well as setup instructions.

# Incentive Mechanism

As described above, each Miner reports its MinerIndex to the Validator. The MinerIndex details how much and what type of data the Miner has. The Miner is then scored based on 2 dimensions:
1. How much data the Miner has and how valuable that data is.
1. How credible the Miner is.

## Data Value

Not all data is equally valuable! There are several factors used to determine data value:

### 1) Data Freshness

Fresh data is more valuable than old data, and data older than a certain threshold is not scored.

As of Dec 11th, 2023 data older than 30 days is not scored. This may increase in future.

### 2) Data Desirability

Data Universe defines a [DataDesirabilityLookup](https://github.com/RusticLuftig/data-universe/blob/main/rewards/data_desirability_lookup.py) that defines which types of data are desirable. Data deemed desirable is scored more highly. Unspecified labels get the default_scale_factor of 0.5 meaning they score half value in comparison.

The DataDesirabilityLookup will evolve over time, but each change will be announced ahead of time to give Miners adequate time to prepare for the update.

### 3) Duplication Factor

Data that's stored by many Miners is less valuable than data stored by only a few. The value of a piece of data is decreases proportional to the number of Miners storing it.

## Miner Credibility

Validators remain suspicious of Miners and so they periodically check a sample of data from each Miner's MinerIndex, to verify the data correctness. The Validator uses these checks to track a Miner's credibility, which it then uses to scale a Miner's score. The scaling is done in such a way that it is **always** worse for a Miner to misrepresent what types and how much data it has.

# Data Universe Dashboard

As you can see from the above, Data Universe rewards diversity of data (storing 200 copies of the same data isn't exactly beneficial!) 

To help understand the current data on the Subnet, the Data Universe team hosts a dashboard (https://shorturl.at/Ca5uu), showing the amount of each type of data (by DataEntityBucketId) on the Subnet. Miners are strongly encouraged to use this dashboard to customize their [Miner Configuration](./docs/miner.md#configuring-the-miner), to maximize their rewards.

# Getting Started

See [Miner Setup](docs/miner.md#miner_setup) to learn how to setup a Miner.

See [Validator Setup](docs/validator.md#validator_setup) to learn how to setup a Validator.

# Upcoming Features

1. A Validator API to allow other Subnets to query the data.
2. More data sources

# Terminology

**DataDesirabilityLookup:** A [defined list of rules](https://github.com/RusticLuftig/data-universe/blob/main/rewards/data_desirability_lookup.py) that determine how desirable data is, based on its DataSource and DataLabel.

**DataEntity:** A single "item" of data collected by a Miner. Each DataEntity has a URI, that the Validators can use to retrieve the item from its DataSource.

**DataEntityBucket:** A logical grouping of DataEntities, based on its DataEntityBucketId.

**DataEntityBucketId:** The unique identifier for a DataEntityBucket. It contains the TimeBucket, DataSource, and DataLabel.

**DataLabel:** A label associated with a DataEntity. Precisely what the label represents is unique to the DataSource. For example, for a Yahoo finance DataSource, the label is the stock ticker of the finance data.

**DataSource:** A source from which Miners scrape data.

**Miner Credibility**: A per-miner rating, based on how often they pass data validation checks. Used to heavily penalize Miner's who misrepresent their MinerIndex.

**Miner Index**: A summary of how much and what types of data a Miner has. Specifically, it's a list of DataEntityBuckets.
"""

compute_roadmap = """
# Compute Subnet on Bittensor

Welcome to the **Compute Subnet on Bittensor**! This project enables a decentralized, peer-to-peer GPU rental marketplace, connecting miners who contribute GPU resources with users who need computational power. Our frontend interface is available at [computenet.ai](https://computenet.ai), where you can easily rent machines from the subnet.

## Table of Contents

- [Introduction](#introduction)
- [High-Level Architecture](#high-level-architecture)
- [Getting Started](#getting-started)
  - [For Renters](#for-renters)
  - [For Miners](#for-miners)
  - [For Validators](#for-validators)
- [Contact and Support](#contact-and-support)

## Introduction

The Compute Subnet on Bittensor is a decentralized network that allows miners to contribute their GPU resources to a global pool. Users can rent these resources for computational tasks, such as machine learning, data analysis, and more. The system ensures fair compensation for miners based on the quality and performance of their GPUs.


## High-Level Architecture

- **Miners**: Provide GPU resources to the network, evaluated and scored by validators.
- **Validators**: Securely connect to miner machines to verify hardware specs and performance. They maintain the network's integrity.
- **Renters**: Rent computational resources from the network to run their tasks.
- **Frontend (computenet.ai)**: The web interface facilitating easy interaction between miners and renters.
- **Bittensor Network**: The decentralized blockchain in which the compensation is managed and paid out by the validatators to the miners through its native token, $TAO.

## Getting Started

### For Renters

If you are looking to rent computational resources, you can easily do so through the Compute Subnet. Renters can:

1. Visit [computenet.ai](https://computenet.ai) and sign up.
2. **Browse** available GPU resources.
3. **Select** machines based on GPU type, performance, and price.
4. **Deploy** and monitor your computational tasks using the platform's tools.

To start renting machines, visit [computenet.ai](https://computenet.ai) and access the resources you need.

### For Miners

Miners can contribute their GPU-equipped machines to the network. The machines are scored and validated based on factors like GPU type, number of GPUs, bandwidth, and overall GPU performance. Higher performance results in better compensation for miners.

If you are a miner and want to contribute GPU resources to the subnet, please refer to the [Miner Setup Guide](neurons/miners/README.md) for instructions on how to:

- Set up your environment.
- Install the miner software.
- Register your miner and connect to the network.
- Get compensated for providing GPUs!
"""

omega_roadmap = """
## Introduction

Welcome to the OMEGA Labs Bittensor subnet, a groundbreaking initiative that aims to create the world's largest decentralized multimodal dataset for accelerating Artificial General Intelligence (AGI) research and development. Our mission is to democratize access to a vast and diverse dataset that captures the landscape of human knowledge and creation, empowering researchers and developers to push the boundaries of AGI.

By harnessing the power of the Bittensor network and a global community of miners and validators, we are building a dataset that surpasses the scale and diversity of existing resources. With over 1 million hours of footage and 30 million+ 2-minute video clips, the OMEGA Labs dataset will enable the development of powerful AGI models and transform various industries.


## Key Features

- 🌍 **Unparalleled Scale and Diversity**: 1 million+ hours of footage, 30 million+ video clips, covering 50+ scenarios and 15,000+ action phrases.
- 🧠 **Latent Representations**: Leveraging state-of-the-art models to translate video components into a unified latent space for efficient processing.
- 💰 **Incentivized Data Collection**: Rewarding miners for contributing high-quality, diverse, and novel videos through a decentralized network.
- 🤖 **Empowering Digital Agents**: Enabling the development of intelligent agents that can navigate complex workflows and assist users across platforms.
- 🎮 **Immersive Gaming Experiences**: Facilitating the creation of realistic gaming environments with rich physics and interactions.

## Miner and Validator Functionality

### Miner

- Performs a simple search on YouTube and retrieves 8 videos at a time.
- Provides a certain clip range (maximum of 2 minutes) and a description (catch) which includes the title, tags, and description of the video.
- Obtains the ImageBind embeddings for the video, audio, and caption.
- Returns the video ID, caption, ImageBind embeddings (video, audio, caption embeddings), and start and end times for the clips (maximum of 2 minutes).

### Validator

- Takes the received videos from the miners and randomly selects one video for validation.
- Computes the ImageBind embeddings for all three modalities (video, audio, caption) of the selected video.
- Compares the quality of the embeddings to ensure they are consistent with the miner's submissions.
- If the selected video passes the validation, assumes all eight videos from the miner are valid.
- Scores the videos based on relevance, novelty, and detail richness:
  - Relevance: Calculated using cosine similarity between the topic embedding and each of the eight videos.
  - Novelty: For each video, finds the closest video in the Pinecone index and computes 1 - similarity.
    - Potential issue: Choosing the second most similar video instead of the most similar one.
  - Detail Richness: Determined by the cosine similarity between the text and video embeddings.
- Collects 1024 validated video entries and pushes them to Hugging Face as a file, which is then concatenated.
  - If a miner submits too frequently, the validator may increase the file threshold accumulation limit.
  - If the API needs to shut down for any reason, it will submit the remaining validated entries.

## SN24: Ω Focus Videos Submission

We're excited to introduce a new feature in the SN24 ecosystem: the Focus Video submission and reward process. This system creates a robust marketplace for task-completion videos, leveraging the strengths of the Bittensor network. Here's how it works:

### The Players
1. Ω Focus users: Individuals who complete tasks and record their work
2. SN24 miners: Network participants who can purchase Focus videos
3. SN24 validators: Entities that validate and score submissions
4. Ω Brain: Ω Focus's backend API that processes submissions

### The Process

#### 1. Task Completion and Recording
Ω Focus users create tasks for themselves within the app. They then complete these tasks while screen recording their work via the app.

#### 2. Submission and Initial Processing
Once a task is completed, the user's screen recording and task metadata are uploaded to Ω Brain. This backend system processes the recording, extracting metadata and combining partial clips if necessary.

#### 3. Scoring
Ω Brain forwards the processed video to the SN24 validator API. The validator scores the submission based on predefined criteria. To learn more about the scoring algorithm, check out [this section](#scoring-algorithm) below.

#### 4. User Notification and Marketplace Listing
The Ω Focus user receives their score and an estimate of the potential TAO reward. They can then choose to submit their video to the SN24 Focus Videos marketplace.

#### 5. Miner Purchase
SN24 miners can browse and purchase videos from the marketplace. To make a purchase, a miner notifies the SN24 validator API of their intent. The API informs the miner of the TAO amount to transfer to the Ω Focus user's wallet. [Code here](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/focus_app_v1_integration/purchase_focus_video.py)

#### 6. Transaction Verification
Once the miner transfers the TAO, they provide the transaction's block hash to the SN24 validator API. The API then verifies this transaction on the Bittensor chain's public ledger. [Code here](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/8ecf61b5846e2eb226aaa30f01e23df850f3c435/validator-api/validator_api/cron/confirm_purchase.py#L55)

#### 7. Miner Scoring and Reimbursement
SN24 validators, while sending their YouTube scraping requests to miners, also check with the validator API to see if miners have purchased Focus Videos. Miners' scores are adjusted based on these purchases. Via validators increasing the miners' scores for purchasing videos from the marketplace, the Bittensor chain effectively then reimburses miners for their Focus Video purchases over the following 24-hour period. [Code here](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/8ecf61b5846e2eb226aaa30f01e23df850f3c435/omega/base/validator.py#L322-L326)

#### 8. Impact on Miner Scores
Focus Video scores currently make up 2.5% of a miner's total SN24 score. We plan to increase this percentage as the system proves successful.

#### 9. Video Availability for External Buyers
Once a Focus Video submission is marked as COMPLETED (which happens when a miner transfers TAO to the Ω Focus user), the video becomes available for purchase by external data buyers, such as AI research labs. (Note: This feature will be implemented in the future.)

### Benefits
- Users are incentivized to complete and record valuable tasks
- Miners can improve their scores by purchasing high-quality Focus Videos
- The network gains a new source of verified, high-quality data
- External entities will gain access to a marketplace of task-completion videos

We believe this system will create a vibrant ecosystem within SN24, driving value for all participants while generating useful data for the broader AI community. We're starting with a conservative 2.5% score impact for Focus Videos, but we're excited to see how this new feature develops and grows within our network.

```mermaid
flowchart TD
    A["👤 Ω Focus User"] -->|"1️⃣ Complete task & record"| B
    B["🧠 Ω Brain"] -->|"2️⃣ Process video"| C
    C{"🛡️ SN24 Validator API"}
    C -->|"3️⃣ Score submission"| A
    A -->|"4️⃣ List video"| E["🎥 Focus Videos Marketplace"]
    F["⛏️ SN24 Miner"] -->|"5️⃣ Purchase video"| E
    F -->|"6️⃣ Transfer TAO"| G["💰 User Wallet"]
    F -.->|"7️⃣ Provide tx hash"| C
    C -.->|"8️⃣ Verify transaction"| I
    I["🔍 SN24 Validator"] -.->|"9️⃣ Check purchases & set weights"| H{"⛓️ Bittensor Chain"}
    H -.->|"🔟 Reimburse miners"| F

    classDef user fill:#30336b,stroke:#333,stroke-width:2px,color:white;
    classDef brain fill:#eeac99,stroke:#333,stroke-width:2px,color:white;
    classDef api fill:#e06377,stroke:#333,stroke-width:2px,color:white;
    classDef market fill:#c83349,stroke:#333,stroke-width:2px,color:white;
    classDef miner fill:#5b9aa0,stroke:#333,stroke-width:2px,color:white;
    classDef validator fill:#f0932b,stroke:#333,stroke-width:2px,color:white;
    classDef chain fill:#6ab04c,stroke:#333,stroke-width:2px,color:white;
    classDef external fill:#61c0bf,stroke:#333,stroke-width:2px,color:white;

    class A user;
    class B brain;
    class C api;
    class D,E market;
    class F miner;
    class G user;
    class H chain;
    class I validator;
    class J external;
```

### Scoring Algorithm

A task completion video's final score is a geometric average of five components:

#### gemini based scores
1. task_gemini_score: Gemini's evaluation of the task's quality, based on the task overview and how it feeds into the community's goals and its relevance to teaching AI systems ([prompt](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/8ecf61b5846e2eb226aaa30f01e23df850f3c435/validator-api/validator_api/services/focus_scoring_prompts.py#L2))
2. completion_gemini_score: Gemini's evaluation of how well the task was completed and how relevant the video content is to the task and the community's goals ([prompt](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/8ecf61b5846e2eb226aaa30f01e23df850f3c435/validator-api/validator_api/services/focus_scoring_prompts.py#L88))

#### embeddding based scores
3. task_uniqueness_score: Uniqueness of the task based on embedding similarity of the task overview with existing tasks in the system
4. description_uniqueness_score: Uniqueness of the video description based on embedding similarity of the detailed video description with existing video annotations in the system
5. video_uniqueness_score: Uniqueness of the video content based on embedding similarity of the video with existing videos in the system

Each component contributes equally to the final score. We chose to use a geometric average to ensure that no individual component dominates the final score.

You can dig into the code implementation [here](https://github.com/omegalabsinc/omegalabs-bittensor-subnet/blob/8ecf61b5846e2eb226aaa30f01e23df850f3c435/validator-api/validator_api/services/scoring_service.py#L240).

### Why so Complicated?

Anyone experienced with Bittensor is probably asking themselves right now: why is this video submission process so convoluted? Why not just have Ω Focus users be miners and be compensated directly via the Bittensor chain's emissions each epoch? There are a few reasons:

1. Bittensor’s emissions system awards miners constantly (every epoch), and miners who do not perform well are eventually deregistered and must buy in again (optimized for consistently high performance and throughput). We see Ω Focus users completing tasks and submitting their screen recordings with irregular schedules (some days you do awesome work, some days you rest). With less consistent schedules, we don’t want temporarily inactive users to be deregistered (and subsequently have to re-register to start earning again).
2. Therefore, Ω Labs and SN24 miners acts as intermediaries. Ω Focus users complete tasks and submit their recordings on an arbitrary schedule while SN24 miners are consistently buying up available screen recordings and submitting them to SN24 validators for verification.
3. Once smart contracts are available on Bittensor, as Const mentioned recently, we will definitely move over to emitting rewards directly to Focus users in a fully decentralized manner.

### Hmmm, this doesn't feel like it's fully decentralized

Yes, we acknowledge that. Even while Smart Contracts are not available on Bittensor, there is still room for us to decentralize the scoring and purchase verification process further. Some next steps here include:

1. Use some decentralized database to store the Focus Video scores, annotations, and purchase status.
2. Move the scoring to run locally on the validator's machines via opensource video understanding models like Qwen2-VL-72b when it becomes available or by simply having validators make requests to the Gemini API themselves in the meantime.
3. Creating a public dashboard where anyone in the Bittensor community can view the Focus Videos and their associated scores to judge for themselves the quality of the submissions.

All in all, this is an MVP release and we wanted to just ship something out to get the ball rolling. We are 100% committed to decentralizing the system as much as possible urgently, but also want to emphasize the novel nature of what we're implementing here and appreciate everyone's patience as we make the system more robust and decentralized.

Learn more about the Ω Focus app in [this FAQ](https://focus.omega.inc).

## Roadmap

### Phase 1: Foundation (Q1 2024)
- [x] Launch OMEGA Labs subnet on Bittensor testnet
- [x] Reach 100,000 hours of footage and 3 million video clips

### Phase 2: Expansion (Q2 2024)
- [x] Reach 250,000 hours of footage and 15 million video clips
- [x] Train and demo any-to-any models on the dataset
- [ ] Build synthetic data pipelines to enhance dataset quality
- [ ] Publish a research paper on the Bittensor-powered Ω AGI dataset
- [ ] Expand into running inference for state-of-the-art any-to-any multimodal models

### Phase 3: Refinement (Q3 2024)
- [ ] Reach 500,000+ hours of footage and 30 million+ video clips
- [ ] Use the dataset to train powerful unified representation models
- [ ] Fine-tune any-to-any models for advanced audio-video synchronized generation
- [ ] Open up an auctioning page for companies and groups to bid on validation topics using various currencies (in addition to TAO)
- [ ] Develop state-of-the-art video processing models for applications such as:
  - Transcription
  - Motion analysis
  - Object detection and tracking
  - Emotion recognition

### Phase 4: Application (Q4 2024)
- [ ] Train desktop & mobile action prediction models on the dataset
- [ ] Develop cross-platform digital agents MVP

### Phase 5: Democratization (Q1 2025)
- [ ] Generalize the subnet for miners to upload videos from any data source
- [ ] Incentivize people to record and label their own data using non-deep learning approaches

#### Tips for Better Incentive
The subnet has become quite competitive, and the basic miner template is no longer sufficient to earn good emissions and avoid deregistration. Here are some tips to consider improving your miner:
1. Use proxies or frequently change your pod.
  a) We've heard good things about [Storm Proxies](https://stormproxies.com/).
2. Make sure your videos are unique. You can de-duplicate your collected video with this [video ID index](https://huggingface.co/datasets/jondurbin/omega-multimodal-ids) graciously offered by Jon, one of the miners on the OMEGA subnet.
3. Improve the descriptions you are submitting alongside your uploaded videos. You can try doing this by using video captioning models or incorporating the transcript. Lots of experimentation room here.
4. You can use the `check_score` endpoint that we offer to check your score breakdown. See [this gist](https://gist.github.com/salmanshah1d/f5a8e83cb4af6444ffdef4325a59b489).
"""

prop_trading_roadmap = """
### Subnets

Subnets are decentralized networks of machines that collaborate to train and serve machine learning models.

### Miners

Miners run machine learning models. They send signals to the Validators.

### Validators

Validators recieve trade signals from Miners. Validators ensure trades are valid, store them, and track portfolio returns. 

</details>

<br />
<br />

# Proprietary Trading Subnet

This repository contains the code for the Proprietary Trading Network (PTN) developed by Taoshi.

PTN receives signals from quant and deep learning machine learning trading systems to deliver the world's
most complete trading signals across a variety of asset classes.

# Features

🛠️&nbsp;Open Source Strategy Building Techniques (In Our Taoshi Community)<br>
🫰&nbsp;Signals From a <a href="https://github.com/taoshidev/proprietary-trading-network/blob/main/vali_objects/vali_config.py#L19"> Variety of Asset Classes</a> - Forex+Commodities, Equities, Crypto<br>
📈&nbsp;<a href="https://taomarketcap.com/subnet/8?subpage=miners&metagraph_type=miners">Millions of $ Payouts</a> to Top Traders<br>
💪&nbsp;Innovative Trader Performance Metrics that Identify the Best Traders<br>
🔎&nbsp;<a href="https://dashboard.taoshi.io/">Trading + Metrics Visualization Dashboard</a>

## How does it work?

PTN is the most challenging & competitive network in the world. Our miners need to provide futures based signals (
long/short)
that are highly efficient and effective across various markets to compete (forex, crypto, equities). The top miners are
those that provide the most returns, while never exceeding certain drawdown limits.

### Rules

1. Miners can submit LONG, SHORT, or FLAT signal for Forex, Crypto, and Equities trade pairs into the network. <a href="https://github.com/taoshidev/proprietary-trading-network/blob/main/vali_objects/vali_config.py#L173">Currently supported trade pairs</a>
2. Orders outside of market hours are ignored. 
3. Miners can only open 1 position per trade pair/symbol at a time.
4. Positions are uni-directional. Meaning, if a position starts LONG (the first order it receives is LONG), 
it can't flip SHORT. If you try and have it flip SHORT (using more leverage SHORT than exists LONG) it will close out 
the position. You'll then need to open a second position which is SHORT with the difference.
5. Position leverage is bound per trade_pair. If an order would cause the position's leverage to exceed the upper boundary, the position leverage will be clamped. Minimum order leverage is 0.001. Crypto positional leverage limit is [0.01, 0.5]. Forex/Equities positional leverage limit is [0.1, 5]
6. Leverage is capped at 10 across all open positions in a miner's portfolio. Crypto position leverages are scaled by 10x when contributing
to the leverage cap. <a href="https://docs.taoshi.io/tips/p10/">View for more details and examples.</a>
7. You can take profit on an open position using LONG and SHORT. Say you have an open LONG position with .5x 
leverage and you want to reduce it to a .25x leverage position to start taking profit on it. You would send in a SHORT signal
of size .25x leverage to reduce the size of the position. LONG and SHORT signals can be thought of working in opposite 
directions in this way.
8. Miners can explicitly close out a position by sending in a FLAT signal. 
9. Miners are eliminated if they are detected as plagiarising other miners. (more info in  the "Eliminations" section).
10. There is a fee per order "spread fee". The fee scales with leverage. e.x a 3x leveraged order will have a 3x higher fee.
11. There is a fee for leaving positions open "carry fee". The fee is equal to 10.95/5.25/3% per year for a 1x leverage position (crypto/equities/forex) <a href="https://docs.taoshi.io/tips/p4/">More info</a>
12. There is a minimum registration fee of 2.5 TAO on the mainnet subnet.
13. There is an immunity period of 9 days to help miners submit orders to become competitive with existing miners. Eliminated miners do not benefit from being in the immunity period.
14. Based on portfolio metrics such as omega score and total portfolio return, weights/incentive get set to reward the best miners.

With this system only the world's best traders & deep learning / quant based trading systems can compete.


# Eliminations

In the Proprietary Trading Network, Eliminations occur for miners that commit Plagiarism.


### Plagiarism Eliminations

Miners who repeatedly copy another miner's trades will be eliminated. Our system analyzes the uniqueness of each submitted order. If an order is found to be a copy (plagiarized), it triggers the miner's elimination.

### Post-Elimination

After elimination, miners are not immediately deregistered from the network. They will undergo a waiting period, determined by registration timelines and the network's immunity policy, before official deregistration. Upon official deregistration, the miner forfeits registration fees paid.
"""

protein_folding_roadmap = """
# Introduction
The protein folding subnet is Bittensors’ first venture into academic use cases, built and maintained by [Macrocosmos AI](https://www.macrocosmos.ai). While the current subnet landscape consists of mainly AI and web-scraping protocols, we believe that it is important to highlight to the world how Bittensor is flexible enough to solve almost any problem.

This subnet is designed to produce valuable academic research in Bittensor. Researchers and universities can use this subnet to simulate almost any protein, on demand, for free. It is our hope that this subnet will empower researchers to conduct world-class research and publish in top journals while demonstrating that decentralized systems are an economic and efficient alternative to traditional approaches.


# What is Protein Folding?  

  Proteins are the biological molecules that "do" things, they are the molecular machines of biochemistry. Enzymes that break down food, hemoglobin that carries oxygen in blood, and actin filaments that make muscles contract are all proteins. They are made from long chains of amino acids, and the sequence of these chains is the information that is stored in DNA. However, its a large step to go from a 2D chain of amino acids to a 3D structure capable of working. 

  The process of this 2D structure folding on itself into a stable, 3D shape is called **protein folding**. For the most part, this process happens naturally and the end structure is in a much lower free energy state than the string. Like a bag of legos though, it is not enough to just know the building blocks being used, its the way they're supposed to be put together that matters. *"Form defines function"* is a common phrase in biochemsitry, and it is the quest to determine form, and thus function of proteins, that makes this process so important to understand and simulate. 

# Why is Folding a Good Subnet Idea? 
An ideal incentive mechanism defines an asymmetric workload between the validators and miners. The necessary proof of work (PoW) for the miners must require substantial effort and should be impossible to circumvent. On the other hand, the validation and rewarding process should benefit from some kind of privileged position or vantage point so that an objective score can be assigned without excess work. Put simply, **rewarding should be objective and adversarially robust**.

Protein folding is also a research topic that is of incredibly high value. Research groups all over the world dedicate their time to solving particular niches within this space. Providing a solution to attack this problem at scale is what Bittensor is meant to provide to the global community. 

# Simulation Backend and Reproducability
Moleccular dynamics (MD) simulations require a physics-based engine to run them, and SN25 utilizes the open-source project [OpenMM](https://openmm.org). As their tagline suggests, they are a "high performance, customizable molecular simulation" package. 

One of the key advantages of using OpenMM for MD-simulations is the built-in capabilities for *reproducability*. This is a key component in the reward stack and all miners should be intimately familiar with this. For more information, please read this [document](./documentation/reproducibility.md). 

# Reward Mechanism
Protein folding is a textbook example of this kind of asymmetry; the molecular dynamics simulation involves long and arduous calculations which apply the laws of physics to the system over and over again until an optimized configuration is obtained. There are no reasonable shortcuts. 

While the process of simulation is exceedingly compute-intensive, the evaluation process is actually straightforward. **The reward given to the miners is based on the ‘energy’ of their protein configuration (or shape)**. The energy value compactly represents the overall quality of their result, and this value is precisely what is decreased over the course of a molecular dynamics simulation. The energy directly corresponds to the configuration of the structure, and can be computed in closed-form. The gif below illustrates the energy minimization over a short simulation procedure.

When the simulations finally converge (ΔE/t < threshold), they produce the form of the proteins as they are observed in real physical contexts, and this form gives rise to their biological function. Thus, the miners provide utility by preparing ready-for-study proteins on demand. An example of such a protein is shown below. 

## How does the Subnet Work?

In this subnet, validators create protein folding challenges for miners, who in turn run simulations using OpenMM to obtain stable protein configurations. At a high level, each role can be broken down into parts: 

### Validation

1. Validator creates a `neuron.queue_size` number of proteins to fold.
2. These proteins get distributed to a `neuron.sample_size` number of miners (ie: 1 PDB --> sample_size batch of miners).
3. Validator is responsible for keeping track of `sample_size * queue_size` number of individual tasks it has distributed out. 
4. Validator queries and logs results for all jobs based on a timer, `neuron.update_interval`. 

For more detailed information, look at [validation.md](./documentation/validation.md)
"""

dippy_roadmap = """
## Introduction

> **Note:** The following documentation assumes you are familiar with basic Bittensor concepts: Miners, Validators, and incentives. If you need a primer, please check out https://docs.bittensor.com/learn/bittensor-building-blocks.

Dippy is one of the world's leading AI companion apps with **1M+ users**. The app has ranked [**#3 on the App Store**](https://x.com/angad_ai/status/1850924240742031526) in countries like Germany, been covered by publications like [**Wired magazine**](https://www.wired.com/story/dippy-ai-girlfriend-boyfriend-reasoning/) and the average Dippy user **spends 1+ hour on the app.** 

The Dippy Roleplay subnet on Bittensor aims to create the world's best open-source roleplay LLM by leveraging the collective efforts of the open-source community. This subnet addresses the critical issue of loneliness, which affects a significant portion of the population and is linked to various mental and physical health problems. 

Current SOTA LLMs (Claude, OpenAI etc.) are designed for the assistant use case and lack the empathetic qualities necessary for companionship. While some companies (like Character AI and Inflection) have developed closed-source roleplay LLMs, the open-source alternatives lag significantly behind in performance. 

![DIPPY](/assests/comp.png)

## Roadmap

Given the complexity of creating a state of the art roleplay LLM, we plan to divide the process into 3 distinct phases.

**Phase 1:** 
- [x] Subnet launch with robust pipeline for roleplay LLM evaluation on public datasets and response length 
- [x] Public model leaderboard based on evaluation criteria
- [x] Introduce Coherence and Creativity as a criteria for live model evaluation

**Phase 2:** 
- [ ] Publicly release front-end powered by top miner submitted model of the week
- [ ] Segment model submission into different "expert" categories (funny, romantic, therapeutic etc)
- [ ] Models with the highest score in each personality type are chosen as "expert" models and made publicly available on the front-end

**Phase 3:** 
- [ ] New Mixture of Experts model made as a baseline based on the "expert" models chosen from Phase 2
- [ ] Robust pipeline to evaluate new MOE model submissions against live evaluation criteria
- [ ] Expand the state of the art in roleplay LLMs through continuous iteration and data collection

## Overview of Miner and Validator Functionality

**Miners** would use existing frameworks, fine tuning techniques, or MergeKit, to train, fine tune, or merge models to create a unique roleplay LLM. These models would be submitted to a shared Hugging Face pool. 

**Validators** would evaluate the and assess model performance via our protocol and rank the submissions based on various metrics (empathy, conciseness etc). We will provide a suite of 
testing and benchmarking protocols with state-of-the-art datasets.

#### Submitting a model
As a miner, you're responsible for leveraging all methods available at your disposal, including but not limited to training new models, merging existing models (we recommend [MergeKit](https://github.com/arcee-ai/mergekit)), finetuning existing models, and so on to push roleplay LLMs forward.

We outline the following criteria for Phase 1:

- Models should be 7B-13B parameters. Current maximum model size is 32GB. 
- We don't support quantized models at the moment...coming soon!
- Models MUST be Safetensors Format! Check upload_models.py for how the model upload precheck works.
- Please test the model by loading model using transformers.AutoModelForCausalLM.from_pretrained
- (Recommended) Test the model with arbitrary inputs, before submitting, to check for NaNs.
- Models we are confident will work are of the Mistral-7B and Llama-3 8B family.
- We support the "alpaca", "chatml", "llama2", "llama3", "mistral", "vicuna" and "zephyr" chat templates.

Once you're happy with the performance of the model for the usecase of Roleplay, you can simply submit it to Hugging Face 🤗 and then use the following command:

## Model Evaluation Criteria
### Model Size
A smaller model will score higher than a big model. Model size is the disk space occupied by the model repo from HF. The max model size is limited to 72GB.

<!-- $S_{size} = 1 - ModelSize/ MaxModelSize$ -->
### Latency
A faster model will score higher than a slow model.

### Output Similarity
Evaluated against datasets, a model that generates similiar resposne to groundtruth will score higher.

### Vibe Matching
A model that can generate outputs with similiar length to its inputs will score higher.

## Acknowledgement

Our codebase is built upon [Nous Research's](https://github.com/NousResearch/finetuning-subnet) and [MyShell's](https://github.com/myshell-ai/MyShell-TTS-Subnet?tab=readme-ov-file) Subnets.
"""

nas_roadmap = """
## Introduction

Neural Architecture Search (NAS) is a critical field in machine learning that focuses on automating the design of artificial neural network architectures. As deep nerual network models become increasingly complex and computationally expensive, the significance of NAS grows. The primary goal of NAS is to identify the optimal model that not only maximizes accuracy for a given use-case but also minimizes the number of parameters and the computational cost, measured in Floating Point Operations (FLOPs). However, performing such searches can be very resource-intensive, often requiring days or weeks of computation on hundreds of GPUs to find an optimal model.

NASChain aims to address these challenges by leveraging the power of the Bittensor network and an innovative incentive mechanism. This approach distributes NAS tasks among participants (referred to as miners), thereby decentralizing the computational effort and potentially reducing the time and resources required for finding efficient and effective neural architectures.

---
## How it works

1. **Miners Running NAS Algorithm:** Miners execute the Neural Architecture Search (NAS) algorithm on the dataset described by the sample mining code. The objective of the NAS is to minimize the number of parameters while maximizing accuracy on the test set. NSGA-Net based NAS models are supported by validators and provide a good starting point for miners to run multi-objective optimization.


2. **Model Submission:** Miners upload their best models to Hugging Face with the miner code and submit the metadata for the commit to the blockchain.

3. **Validation Process:** Validators sync with the blockchain, download all models from the miners, and evaluate them on the test set. Architectures that lie on the Pareto Optimal line will have their weights reset and undergo further training by validators on the standard train/valid set to ensure no test set leakage occurred during the miners' model training.

4. **Rewards for Miners:** Miners who produce models that lie on the Pareto Optimal line will be rewarded. Miners task is to train models that maximize accuracy on the test set and minimize the number of parameters.

# Model Training and Validation Rules

### 1. Leaking Test Set to Training Set
Leaking the test set to the training set to gain higher accuracy when evaluated by the validators is considered cheating. Models selected as top models due to their high accuracy on the test set will have their weights reinitialized and retrained with a standard train-test split by the validators. If the submitted model's accuracy is lower than the accuracy achieved by retraining by the validator, the miner will be disqualified.

### 2. Overtraining the Model and Custom Hyperparameters
Please take some time to review `dummy_trainer.py`, `vali_trainer.py`, and `vali_config.py`. Follow the hyperparameters used for training, such as the number of epochs, optimizer, and learning scheduler. Validators will evaluate your model based on `vali_trainer.py` and `vali_config.py`. Your model should outperform other models under the same fair conditions. For example, if you train your model for 500 epochs and achieve 95% accuracy, but the validator only trains the model for 50 epochs before evaluation, your pre-evaluation and post-evaluation results will not match, resulting in disqualification.

### 3. Custom Layer Implementation Not Supported by PyTorch Load and Deserialize Functions
Your models should be loadable and trainable using the generic torch.load() or torch.jit.load() methods. Custom layer implementations that require a layer definition alongside the model weights are not currently supported unless TorchScript can successfully save and load the model.

### 4. Model File Size
NAS is about training small models. There is a file size limit that you can upload as described in `vali_config.py`. Uploading larger model sizes than the limit will be rejected by the validator code. Exceptions will also be thrown during miner model upload if the size exceeds the limit. This limitation is to prevent overloading the validator with models that have billions of parameters unnecessarily for the dataset.

### 5. Duplicate Uploads
If the same architecture is uploaded multiple times by the same or different miners and the model is on the Pareto Optimal line and needs to be rewarded, only the miner with the oldest commit date for that model will be rewarded. For example, if two models uploaded to the chain and HF have exactly 500k parameters and 90% accuracy, the miner that uploaded the model first will be rewarded for that model if it is the top model.

"""

infinite_games_roadmap = """
# Forecasting of Future Events

##  Introduction

We incentivize the prediction of future events. The prediction space is based on binary future events such as the one listed on [Polymarket](https://polymarket.com/) and on [Azuro](https://azuro.org/). We are always actively expanding to new markets and providers. We are focused on *judgemental forecasting* rather than *statistical forecasting*. We hence expect the models used by miners to be LLMs. 

### High-level mechanism

Miners submit their predictions to validators. Each prediction has to be done early enough before the event underlying the prediction settles. Once the event settles, the validators that received the prediction score the miner.

## LLMs open new predictive capabilities

Making predictions is a hard task that requires cross-domain knowledge and intuition. It is often limited in explanatory reasoning and domain-specific (the expert in predicting election results will differ from the one predicting the progress in rocket-engine technology) ([1]). At the same time it is fundamental to human society, from geopolitics to economics. 

<!-- The COVID-19 measures for example were based on epidemiological forecasts. Science is another area where prediction is crucial ([2]) to determine new designs or to predict the outcome of experiments (executing one experiment is costly). Such predictions rely on the knowledge of thousands papers and on multidisciplinary and multidimensional analysis (*can a study replicate ? should one use a molecular or behavioral approach?*). -->

LLMs approach or surpass human forecasting abilities. They near on average the crowd prediction on prediction market events ([1]), and surpass humans in predicting neuroscience results ([2]). They are also shown to be calibrated with their predictions i.e confident when right. Through their generalization capabilities and unbounded information processing, LLMs have the potential to automate the prediction process or complement humans. 


### Real-world applications

The value of the subnet first relies in the improvement of the efficiency of prediction markets. This value can be extracted by validators through arbitrage. The validators may obtain a better knowledge of the probability of an event settling and communicate this information to a prediction market by opening a position. 

The first applications built on top of our subnet could be related to prediction markets. A trader could query our market to obtain the most up to date and relevant predictions to their portfolio based on the current news landscape (LLMs would be constantly aggregating the most up to date and relevant news articles). They could then readjust their positions accordingly or trade directly on this information. 

In the long term, a validator could provide paid economic forecasts or more generally the output of any forward-looking task addressed to an LLM ([2]). A customer might then provide a series of paid sub-queries related to the information they aim at retrieving.

<!-- It could also be used by scientists to design their experiment and frame their ideas. For example, the value of a paper often resides in the way the results are presented and cross-analysed. One way resulting in poor conclusions while the other giving good results. An LLM might help detect the adequate framework. -->


## Miners 

Miners compete by sending to the validators a dictionary identifying an event $E$ with their estimation of the probability $p$ that $E$ is realized. For example, $E$ could be *SBF is sentenced to life*. In the case of Polymarket, an event identifier is a [Polymarket condition id](https://docs.polymarket.com/#overview-8). 


### Miner strategy 

A reference providing a **baseline miner** strategy is the article ["Approaching Human Level Forecasting with Langage Models"](https://arxiv.org/html/2402.18563v1?s=35) ([1]). The authors fine-tune an LLM to generate predictions on binary events (including the ones listed on Polymarket) which nears the performance of human forecasters when submitting a forecast for each prediction, and which beats human forecasters in a setting where the LLM can choose to give a prediction or not based on its confidence.

According to the article, the performance of LLMs likely depends significantly on the amount of data they can retrieve for a given prediction. In the study, this performance was likely limited by the finite amount of data one can extract from prediction markets. If our subnet is able to continually produce new synthetic data miners could be able to beat the SoA (average Brier score of 0.179).


## Validators

Validators record the miners' predictions and score them once the events settle. At each event settlement, a score is added to the moving average of the miner's score. This simple model ensures that all validators score the miners at roughly the same time. Importantly, we implement a **cutoff** for the submission time of a prediction. The cutoff is currently set at 24 hours for Polymarket events and at the start of the relevant sporting event on Azuro (think kick-off of a soccer match). The cutoff is needed since as the event nears resolution the probability of the true outcome tends to one.

## Scoring rule
*We are currently using model 2*

Denote by $S(p_i, o_i)$ the quadratic scoring rule (the Brier score) for a prediction $p_i$ of a binary event $E_i$ and where $o_i$ is $1$ if $E_i$ is realized and $0$ otherwise. With a renormalization we have that $S(p_i, 1)= 1- (1-p_i)^2$ if $o_i$ is $1$ and $S(p_i,0)=1-p_i^2$ if $o_i$ is $0$. A quadratic scoring rule is strictly proper i.e it strictly incentivizes miners to report their true prediction. 

### model 1

The validators directly use a **quadratic scoring rule** on the miners' predictions. If the miner predicted that $E_i$ be realized with probability $p_i$, upon settlement of the outcome the validator scores the miner by adding $S(p_i, o_i)$ to their moving average of the miner's score.

We give miners a score of $0$ on the events for which they did not submit a prediction.

### model 2

The validator stores **the time series of the miner's predictions** and computes the Brier score of each element of the time series. It hence obtains a new time series of Brier scores. A number $n$ of intervals is set between the issues date and the resolution date. The validator then computes a **weighted average of the Brier scores**, where the weight is exponentially decreasing with time, in interval $k$ it has value $exp(-\frac{n}{k} +1)$ where $k$ starts at $n$ and decreases to $1$.

The final score is a linear combination of the weighted average and of a linear component that depends on how good is the miner compared to other miners.

This is described in details [here](https://hackmd.io/@nielsma/S1sB8xO_C).


### model 3


We implement a **sequentially shared quadratic scoring rule**. This allows us crucially to aggregate information as well as to score $0$ miners that do not bring new information to the market.
The scoring rule functions by scoring each miner relatively to the previous one. The score of the miner $j$ is then $S_j = S(p_j, o_i) - S(p_{j-1}, o_i)$ where $p_{j-1}$ is the submission of the previous miner. Importantly this payoff can be negative, therefore in practice when aggregating the scores of a miner we add a $\max(-,0)$ operation. 

The aggregated score of a miner that a validator sends to the blockchain is the following:

$$\frac{1}{N} \sum_j S_j$$

where $N$ is the number of events that the validator registered as settled during the tempo.

A simpler version of this model is, instead of paying the miner for their delta to the previous prediction, pay them for their delta to the Polymarket probability at the submission time i.e $S(p_j, o_i) - S(\text{price on polymarket at t}, o_i)$ where $p_j$ is submitted at $t$.

We also want to incorporate a progress or stability component in the scoring rule, as well as not introduce a latency game among miners to submit their predictions (as incentivized by the sequential scoring rule). 

## Roadmap

- Scoring with exponentially decreasing weights until settlement date and linear differentiation mechanism - July 25th 
- Synthetic event generation with central resolution using ACLED data - early August
- Scoring with exponential differentiation mechanism, new entropy scoring component and new improvement rate scoring component - August/September
- Comprehensive and granular analytics - September
- Synthetic event generation from news data using an LLM - September
- Synthetic event generation with central resolution with various API modules: elections API, court rulings - data, space flights 
- Mining competition in partnership with Crunch DAO
- Synthetic event generation with UMA resolution - human verifiers resolve our events through the OOv2 
- Aggregation of miners’ predictions - through simple cutoff for benchmark events 
- Synthetic event generation with trustless resolution using UMA - we use the UMA Data Asserter framework for our event resolutions that then go through a challenge period
- More advanced aggregation mechanism based on sequential scoring 

Other items on our roadmap involve:
- commit-reveal on the miners' predictions
- make the prediction framework more LLM specific and create mechanisms that explicitely generate data for the fine-tuning of prediction focused LLMs
- consider other prediction markets such as Metaculus and Manifold (mostly as benchmark events)
- using Reuters or WSJ headlines for event generation

"""

omega_any_to_any_roadmap = """
## Introduction

**OMEGA Any-to-Any** is a decentralized, open-source AI project built on the Bittensor blockchain by OMEGA Labs. Our mission is to create state-of-the-art (SOTA) multimodal any-to-any models by attracting the world's top AI researchers to train on Bittensor, taking advantage of Bittensor's incentivized intelligence platform. Our goal is to establish a self-sustaining, well-resourced research lab, where participants are rewarded for contributing compute and/or research insight.

**MainNet UID**: 21

## Why Any-to-Any? 🧠📚🌃🎧🎥

- **Multimodal First**: A2A jointly models all modalities (text, image, audio, video) at once, with the belief that true intelligence lies in the associative representations present at the intersection of all modalities.
- **Unified Fundamental Representation of Reality**: The [Platonic Representation Hypothesis](https://phillipi.github.io/prh/) suggests that as AI models increase in scale and capability, they converge towards a shared, fundamental representation of reality. A2A models, by jointly modeling all modalities, are uniquely positioned to capture this underlying structure, potentially accelerating the path towards more general and robust AI.
- **Decentralized Data Collection**: Thanks to our [SN24 data collection](https://github.com/omegalabsinc/omegalabs-bittensor-subnet), we leverage a fresh stream of data that mimics real-world demand distribution for training and evaluation. By frequently refreshing our data collection topics based on gaps in the current data, we avoid the issue of underrepresented data classes (see [this paper](https://arxiv.org/abs/2404.04125) for more discussion on this issue). Through self-play, our SN's best checkpoints can learn from each other and pool their intelligence.
- **Incentivized Research**: World class AI researchers and engineers already love open source. With Bittensor's model for incentivizing intelligence, researchers can be permissionlessly compensated for their efforts and have their compute subsidized according to their productivity.
- **Bittensor Subnet Orchestrator**: Incorporates specialist models from other Bittensor subnets, acting as a high-bandwidth, general-purpose router. By being the best open source natively multimodal model, future AI projects can leverage our rich multimodal embeddings to bootstrap their own expert models.
- **Public-Driven Capability Expansion**: Public demand dictates which capabilities the model learns first through the decentralized incentive structure.
- **Beyond Transformers**: Integrate emerging state-of-the-art architectures like [early fusion transformers](https://arxiv.org/pdf/2405.09818), [diffusion transformers](https://arxiv.org/pdf/2401.08740), [liquid neural networks](https://arxiv.org/pdf/2006.04439), and [KANs](https://arxiv.org/pdf/2404.19756). 

## Roadmap 🚀

### Phase 1: Foundation (Remainder of Q2 2024)

- [x] Design a hard-to-game validation mechanism that rewards deep video understanding
- [ ] Produce the first checkpoint with SOTA image and video understanding capabilities with our ImageBind + Llama-3 architecture as a proof-of-concept starting point
- [ ] Generalize the validation mechanism to enable broad architecture search and new multimodal tokenization methods
- [ ] Onboard 20+ top AI researchers from frontier labs and open source projects
- [ ] Expand SN24 data collection beyond YouTube to include multimodal websites (e.g. Reddit, blogposts) and synthetic data pipelines
- [ ] Launch OMEGA Focus screen recording app, providing rich data for modelling long-horizon human workflows, combatting the hallucination and distraction problem found in top closed-source LLMs

### Phase 2: Fully Multimodal (Q3 2024)

- [ ] Produce the first any-to-any checkpoint natively modelling all modalities that can beat other OSS models on top multimodal and reasoning benchmarks
- [ ] Develop a user-friendly interface for miners and validators to interact with the subnet's top models
- [ ] Onboard 50 more top AI researchers from top labs and open source research collectives
- [ ] Publish a research paper on A2A's architecture, incentive model, and performance
- [ ] Release open source multimodal embedding models (based on our top A2A checkpoint's internal embedding space) for other labs to condition their models on
- [ ] Integrate a framework that can auto-evaluate all the models & commodities produced by other subnets on Bittensor which our top models can then interact with, both through tool-use and through native communication in the latent-space via projection modules

### Phase 3: Exponential Open Research Progress (Q4 2024)

- [ ] Produce the first any-to-any OSS checkpoint that beats all closed-source SOTA general intelligence models
- [ ] Establish partnerships with AI labs, universities, and industry leaders to drive adoption
- [ ] Expand our one-stop-shop Bittensor model evaluation and router framework to arbitrary open source and closed-source checkpoints and APIs
- [ ] Implement task-driven learning, with OMEGA Labs routinely curating high-signal tasks for model trainers to master
- [ ] Start crafting an entirely new "online" validation mechanism that rewards miners for producing agentic models that can complete real-world tasks
- [ ] Use our top checkpoint to power up the multimodal intelligence features of the OMEGA Focus app

### Phase 4: Agentic Focus (Q1 2025)

- [ ] Launch our agent-focused "online" validation mechanism centered around long-range task completion
- [ ] Achieve SOTA performance on agent benchmarks
- [ ] Use OMEGA Focus as an outlet to provide OMEGA digital twin companions to users
- [ ] Launch an app store for A2A-powered applications leveraging our open source models
- [ ] Reach 10M+ users with the OMEGA Focus app

## Current A2A Architecture 🤖

At launch, we are starting with an approach that builds on one of the most powerful and mainstream LLMs as a backbone: Llama 3. A multilayer perceptron (MLP) projects Imagebind embeddings directly into the pretrained Llama 3 internal state, allowing a finetuned model to develop video understanding.

The provided mining repo with default settings will train both:

-  the encoding projection layer, which encodes Imagebind embeddings into Llama 3 states, and
-  a LoRA adapter which allows the underlying LLM to develop multimodal understanding

There are several immediate areas miners can investigate in order to produce a checkpoint with improved multimodal understanding:

- Train for longer,
- Find better hyperparameters: learning rate, optimizer, batch sizes, gradient accumulation, etc.,
- Use additional datasets (more diverse, or even larger than the SN24 dataset),
- Try different LoRA parameters, or finetune all parameters.

In the near future we'll enable much deeper architecture search, allowing researchers to experiment with different LLM backbones, vastly different encoders and decoders.

## The Future of OMEGA A2A 🔮

OMEGA A2A is poised to revolutionize the AI landscape by harnessing the power of Bittensor's incentivized intelligence model and attracting the world's top AI researchers. Our mission is to push the boundaries of what's possible in decentralized AI, focusing on:

- Developing fully multimodal, any-to-any models that outperform all other open-source solutions
- Creating an AI gateway framework to seamlessly integrate and evaluate models from across the Bittensor ecosystem and beyond
- Implementing task-driven learning and agent-focused validation to create models capable of completing complex, real-world tasks
- Powering up the OMEGA Focus app with cutting-edge multimodal intelligence and personalized digital twin companions

As we progress, we will explore fully decentralized infrastructure and governance to ensure a truly democratized AI ecosystem. Our research will explore groundbreaking architectures beyond transformers and attention mechanisms, pushing the limits of AI capabilities.

By hyper-connecting to the Ω SN24, we will access diverse, high-quality data that fuels our models' growth and enables them to tackle a wide range of tasks. Innovative monetization strategies will be implemented to sustain and grow the ecosystem, ensuring long-term success and viability.

Through the tireless efforts of our decentralized OMEGA A2A research collective, we aim to showcase the immense potential of Bittensor's incentivized intelligence model and establish ourselves as leaders in the AI research community and beyond.

Join us on this transformative journey as we shape the future of decentralized AI, unlocking new possibilities and creating a more accessible, powerful, and innovative AI ecosystem for all. :rocket:

## Incentives 🎂

We aim to collectively push forward the SOTA of multimodal and agentic AI research. The incentives in this subnet will evolve as we add modalities and tasks, but they will consistently reflect this underlying goal.

The initial reward structure has two parts:

- Video understanding: can your checkpoint understand and accurately caption video embeddings?
- Language capabilities: does your checkpoint retain the language capabilities of the LLM backbone?

As we improve the incentive scheme over time to create better and more diverse multimodal capabilities, we'll give ample notice and detail of upcoming changes.
"""

bitagent_roadmap = """
Quick Pitch: BitAgent revolutionizes how you manage tasks and workflows across platforms, merging the capabilities of large language models (LLMs) with the convenience of your favorite apps such as web browsers, Discord, and custom integrations. BitAgent empowers users to seamlessly integrate intelligent agents, providing personalized assistance and integrated task automation.

Key Objective - provide intelligent agency to simplify and automate tasks in your day-to-day

GoGoAgent - Our Application - https://gogoagent.ai
MSPTech - Real world business case - https://MSPTech.ai

Key Features

Working our way up the Berkeley Function Calling Leaderboard (BFCL)
No API / subscription requirements
Run light models (8B parameter) for huge impact
FINETUNED MODEL evaluation of tool calling language model fine tunes
MINER HOSTED evaluation of miners running tool calling language models allowing applications to scale on top of SN20
Miner's receive transparent feedback
And a BONUS for getting this far - are you tired of waiting for registration slots? Check out register.sh

## FAQ

Q: How much GPU (VRAM) and RAM do I need to run a validator and/or miner?
A: Validators need a GPU and require a minimum of 48 GBs of VRAM with performant CPU. Miners are left to their own setup, but should be aware that the more capable tool calling LLMs require a decent amount of VRAM (common configurations: a 3090 (with 24GB VRAM) is capable enough for the smaller (~8B params) models we require).

Q: Are there any required subscriptions or paid APIs?
A: No - no subs, no external companies, in fact we'd rather the community build amazing AI capabilities than relying on corporations.

Q: What LLM should I use?
A: This is where the miner needs to experiment some and test and fine-tune different LLM models to find what accomplishes the tasks most successfully. Have a look at models in the Salesforce xLAM family as good starting points.

Q: Validators are running miner-submitted HF models, will validators require trust_remote_code?
A: No, we require that no setup scripts or any code be necessary for running the models.

Q: I started my miner and I am not receiving any tasks.
A: There are a few things to check:

Is your axon port, as reported on the metagraph correct (you can check taostats or metagraph)?
Is your axon port open and reachable from a system in the real world (like where the validators are)?
Do you have Trace logging on to see the dendrite requests and Debug logging on to see the task results?
Make sure your IsAlive() forward is returning True and wait an hour for that to update in the validator's cache.
Make sure there isn't a stale process that is preventing your new miner process from starting up on the intended port.
Q: What about model copying?
A: https://discord.com/channels/799672011265015819/1194736998250975332/1302870011362279514

Q: My model is not being evaluated OFFLINE for FINETUNED SUBMISSION and is receiving a score of 0.
A: There are a few things to check:

Is your model licensed under the apache-2.0 license?
Is your model size less than 10B parameters? We are looking for 8B params or less models.
Is your model name properly set in the Hugging Face?
Q: I'm getting a wallet path error, like: KeyFileError: Keyfile at: ${HOME}/~/.bittensor/wallets/...
A: There is a bug in 8.2.0 that is setting the wallet path incorrectly, so you may need to fix this by adding this parameter to your start command:
--wallet.path ~/.bittensor/wallets

Q: I have a complicated CUDA Device setup and need to use a specific GPU device as a validator running the FINETUNED models:
A: We provide two parameters for this:
--neuron.visible_devices
--neuron.device
Example usage: To use the 2nd CUDA Device, you would add these to your parameters:
--neuron.visible_devices 1 --neuron.device cuda:0

Q: My validator is running out of GPU memory when loading OFFLINE models via sglang.
A: You can use this parameter: --validator-hf-server-mem-fraction-static to increase or decrease the amount of the GPU VRAM to use.
It defaults to 0.55, just over half of the VRAM.

Q: My vLLM or other inference instance is not served on 8000, how do I change this?
A: We provide a parameter --openai-api-base
It defaults to this: http://localhost:8000/v1, updated as needed by passing the --openai-api-base parameter to your start command.

Q: My vTrust is low and it looks like I'm not setting OFFLINE weights.
A: Please test your sglang setup - check here.

Q: I'm validating and seeing errors like:

TimeoutError
ClientConnectorError \
A: These are responses likely during the IsAlive() query, they are just letting you know that the miner is not responding or connecting in time.

Q: My validator is hanging, just printing out "Validator running ..."
A: There are a few things to check:\

Make sure your vLLM is running with the required LLM from vLLM Setup
You may not see much unless you turn on some logging, you can add this to your params to see more details:
--log_level trace --logging.trace --logging.debug
Check your storage, make sure you didn't run out:
df -h
"""

finetuning_roadmap = """
The Finetuning subnet 37 rewards miners for **fine-tuning Large Language Models (LLMs)**. At launch the first competition is evaluated with data generated from a continuous stream of synthetic data provided by [subnet 18](https://github.com/corcel-api/cortex.t/). It is a continuous fine-tuning benchmark, with new data generated daily.

The mechanism works like this:

    1. Miners train and periodically publish models to 🤗 Hugging Face and commit the metadata for that model to the Bittensor chain to sign up for a specific competition and prove the time of training.
    2. Validators download the models from 🤗 Hugging Face for each miner based on the Bittensor chain metadata and continuously evaluate them against the synthetic data. For each competition, only the top model will receive nonzero weights. They also log results to [wandb](https://wandb.ai/opentensor-dev/finetuning).
    3. The Bittensor chain aggregates weights from all active validators using Yuma Consensus to determine the proportion of TAO emission rewarded to miners and validators.

See the [Miner](docs/miner.md) and [Validator](docs/validator.md) docs for more information about how they work, as well as setup instructions.

---

## Incentive Mechanism

Bittensor hosts multiple incentive mechanism through which miners are evaluated by validators for performing actions well. Validators perform the process of evaluation and 'set weights', which are transactions into Bittensor's blockchain. Each incentive mechanism in Bittensor is called a 'subnet'. Weights and the amount of TAO held by the validators become inputs to Bittensor's consensus mechanism called Yuma Consensus. YC drives validators towards a consensus, agreement about the value of the work done by miners. The miners with the highest agreed upon scores are minted TAO, the network digital currency.

Miners within this subnet are evaluated based on the number of times the model they have hosted has a lower loss than another model on the network within the context of a competition. To perform well, miners must attain the lowest loss on the largest number of random batches. For each competition, finding the best model and delta at the earliest block ensures the most incentive.

Note that competitions are specified independently [here](./constants/__init__.py) with a defined split of emissions from the subnet. Competitions each have unique parameters that define which model(s), tokenizer(s), size(s), sequence length(s) and more that miners will be evaluated against.
"""

socialtensor_roadmap = """
# 🎨 NicheImage - Decentralized Image Generation Network 🌐

## Introduction

### Description
NicheImage is a decentralized network that utilizes the Bittensor protocol to enable distributed image generation. This document serves as a guide for setting up and participating in the network, targeting both validators and miners. It includes essential information on project setup, operation, and contribution.

- 📚 [API Documentation](https://docs.nichetensor.com) (API, Roadmap, Technical Descriptions)
- 🏞️ [Miner and Validator Documentation](https://chestnut-radar-416.notion.site/SN23-SocialTensor-Docs-75202763e797465b88f4d395cb1a14ef)
- 🤖 [Taobot](https://interact.tao.bot/social-tensor)
- 📊 [Subnet Statistics & Playground Showcase](https://studio.nichetensor.com/)

### Incentive Distribution

| Category        | Incentive Distribution | Description                                                                                                        |
|-----------------|------------------------|--------------------------------------------------------------------------------------------------------------------|
| 🧭 GoJourney       | 4%                     | Fixed Image Category                                                                                        |
| 🌀 AnimeV3         | 18%                    | Fixed Image Category                                                                                  |
| ⚔️ JuggernautXL | 15%                    | Fixed Image Category                                                            |
| 🏞️ RealitiesEdgeXL  | 19%                    | Fixed Image Category                                                      |
| 💎 Gemma7b         | 3%                     | Fixed Text Category                                                     |
| 🦙 Llama3_70b      | 5%                     | Fixed Text Category|
| 🏷️ StickerMaker    | 3%                     | Fixed Image Category |
| 🌟 SUPIR    | 8%                     | Fixed Image Category |
| 🌟 Kolors | 10% | Fixed Image Category |
| 🌟🌟 FluxSchnell | 12% | Fixed Image Category |
| **Pixtral_12b** | 1% | Fixed Multimodal Category |
| **OpenGeneral** | 1% | [Open category](/docs/open_category_reward_mechanism.md) |
| **OpenDigitalArt** | 1% | [Open category](/docs/open_category_reward_mechanism.md) |

### Key Features
- 🚀 **Decentralized Image Generation Network**: Incentivizing miners to scale up their computational resources, allowing for up to thousands of generations per minute with sufficient GPU resources.
- 📈 **Volume Commitment**: Miners commit to a model type and generation volume.
- 📊 **Fixed And Open Category**: Miners run fixed model list or their own choice for tailored domain.
- 💰 **Incentivized Volume Rewarding Mechanism**: 
  - `new_reward = (category_score - time_penalty) * (0.6 + 0.4 * volume_scale)`
  - `category_score` is the score unique to each model category. It can be:
    - `matching_result` is 0 or 1 based on the similarity matching result with the reproduction of the validator.
    - `t2i_score` is the score from combination of image quality assessment score and prompt adherence score.
  - `time_penalty = 0.4 * (processing_time / timeout)**3`
  - `volume_scale = max(min(total_volume**0.5 / 1000**0.5, 1), 0)`
- 🌟 **Continuous Improvement**: Introducing new models and features based on usage demand.
- 💵 **Earn as a Validator**: Validators can earn money by sharing their request capacity with miners.
"""

omron_roadmap = """
Omron represents a significant stride in enhancing the Bittensor network, aiming to create the world's largest peer-to-peer Verified Intelligence network, by building a Proof-of-Inference system for the Bittensor network. This initiative aligns with the Opentensor foundation's criteria for innovative subnet solutions. zk-ML allows AI models to be converted into a unique 'fingerprint,' a circuit that can be used to verify that a model's prediction was generated by a specific AI model, thereby providing what we term as Proof-of-Inference.

Miners and Validators Functionality
Incentive Mechanism and Reward Structure
Omron incentivizes miners and validators on Subnet 2 to contribute to the generation and validation of high-quality, secure, and efficient verified AI predictions using a specialized reward mechanism that aligns with the unique aspects of zero-knowledge machine learning (zk-ML) and decentralized AI. Currently Zero-knowledge proofs are generally more CPU computationally intensive and opens the opportunity for non-GPU miners to participate however the end goal is to further incentivize the development of proving systems optimized for GPU based operations. The incentives are based around Miners creating succinct and efficient models which can be circuitized with a zero-knowledge proving system.

The reward mechanism for Subnet 2 scores the initial AI predictions based on the cryptographic integrity and time to generate zk-proofs along with the outputs, rather than solely on end results. This approach reduces the computational burden on validators as zk-proofs confirm the source model and integrity of AI predictions efficiently.

Miners
Receive input data from validators on the subnet.
Generate predictions using custom, verifiable AI models that have been converted into zero knowledge circuits
Return the generated content to the requesting validator for validation and distribution.
Validators
Produce input data and distribute requests for verified inference throughout miners participating on the subnet
Confirm that miners are acting faithfully, by verifying the authenticity of the miner's returned zero knowledge proof
Score results from miners based on performance metrics such as proof size and response time
"""

graphite_roadmap = """
What is Graphite? 🔍
Graphite is a specialized subnet designed to handle graphical problems efficiently.

Graphite focuses on the Traveling Salesman Problem (TSP), a classic optimization problem that involves finding the shortest possible route that visits a set of cities and returns to the starting point. This problem is a fundamental challenge in the fields of computer science, mathematics, and operations research as its complexity grows exponentially with the number of cities.


Where does Bittensor fit in? 🧩
Bittensor plays a crucial role in enhancing the capabilities of Graphite. Graphite leverages Bittensor's decentralized machine learning network to efficiently connect miners to handle the computational demands of the TSP and similar graphical problems. This collaboration enables Graphite to provide a robust and scalable infrastructure for solving complex optimization problems.


How does this subnet work? 🤔
Graphite operates as a decentralized network that connects miners and validators to solve graph optimization problems. Currently, synthetic requests are being generated by the validators and sent to miners in the network. Miners are responsible for solving the TSP using the algorithms they have devised and be sent back to the validators to be evaluated.

Graphite AI Logo


Future Development 🔮
We aim to have our own frontend interface where users can input their graph problems and receive solutions from the miners. This will provide a seamless experience for end users to interact with the Graphite subnet and leverage its capabilities to solve complex optimization problems.


Features ✨

Versatile Input Methods ⌨️
We support both coordinate inputs for undirected graphs and edge inputs for directed graphs. This flexibility allows our users to represent their graphical problems in the most intuitive and effective way for their specific use case.


Algorithm Support ⚙️
Instead of our throwing miners to fend for themselves, we provide four different algorithms to assist them in solving the TSP. We have implemented these algorithms for you so it will not be too daunting to begin mining on Graphite.

Algorithm	Description
Nearest Neighbour	A simple and efficient heuristic that builds a tour by repeatedly visiting the nearest unvisited city.
Dynamic Programming	An exact method that solves the problem optimally by breaking it down into smaller subproblems.
Beam Search	A heuristic search algorithm that explores a graph by expanding the most promising nodes.
Hybrid Pointer Network	An advanced deep learning-based approach that combines the strengths of neural networks and traditional optimization techniques.
With that said, to the experienced developers and miners, we encourage you to provide your own algorithms and solvers to improve the performance of the subnet. We have a reward mechanism that incentivizes miners to develop high-performance solvers that outperform the existing algorithms. Read more at Reward Mechanism.


Reward Mechanism 💰
We rewards miners based on their ability to solve graph optimization problems effectively. Miners are incentivized to produce high-quality solutions within a specified timeframe. The rewards are distributed based on the performance of the submitted solutions relative to the best solution in the cohort and a benchmark solution (greedy heuristic). Validators further evaluate the solutions and penalize those that fall short of the performance benchmark.
"""

itsai_roadmap = """
Introduction
Our subnet incentivizes the development of distributed solutions aimed at identifying LLM-generated content.

Given the rapid growth of LLM-generated text, such as ChatGPT's output of 100 billion words daily compared to humans' 100 trillion, we believe that the ability to accurately determine AI-generated text will become increasingly necessary.

Problem
With the recent surge in LLMs appeared many cases where we do actually want to recognize where this text was generated by AI or written by human. Let's explore some scenarios to highlight the potential and significance of LLM detection.

For ML-engineers. Whether you’re sourcing training data, developing a foundational LLM, or fine tuning on your own data, you need to ensure generative text does not make it into your training set. We can help.
For teachers. While tools like ChatGPT offer numerous benefits for the educational sector, they also present opportunities for students to cheat on assignments and exams. Therefore, it is crucial to differentiate between responses authored by genuine students and those generated by LLMs.
For bloggers. Recently many bloggers faced with a lot of ai-generated comments in their social networks. These comments are not really meaningful but attract the attention of their audience and promote unrelated products. With our subnet, you can easily identify which comments are ai-generated and automatically ban them.
And many more, like:

For writers. By utilizing an LLM detection system, writers can assess their text segment by segment to identify sections that appear machine-generated. This enables them to refine these areas to enhance the overall human-like quality of their writing.
For recruiting. Have you also noticed receiving far more applications with lower candidate quality? AI has enabled people to spam hiring teams with artificially written cover letters and assessments. We help you find the candidates who care about your mission and your quality standards.
For cyber security. Scammers can leverage LLMs to quickly and easily create realistic and personalized phishing emails. We can help you determine the provenance of any document or email you’re reviewing.
As you can see there are a lot of areas where AI detection can be very helpful. We believe that creating llm-detection subnet not only provides a useful tool at a good price for people to use, but also encourages competition to make better and smarter ways to spot AI-generated content.

Vision and Roadmap
We've outlined our project objectives and end goals in the Vision & Roadmap document.

Miners
For the baseline model we implemented deberta-v3-large model, which was finetuned on 500k of human/ai-generated texts. Overall accuracy on our validation is about 93%.

Validators
For validating we use two types of data, which is balanced in proportion 1:1.

Human-written texts
To gather human-written validation data we use the Pile dataset.

The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality datasets combined together. It includes web-crawled data, financial, med, law, arxiv, github and also about 15 different topics.

AI-generated texts
For AI-generated text collection, we need to obtain prompts and then generate texts based on these prompts. While for human texts we take samples from Pile dataset we have to generate ai-samples from the same data-source, so that the only difference between them was human/ai written.

So, as prompts we take a random sample and then use part of it as text begging and ask LLMs to generate a completion for it.

We use the Ollama GitHub repository to run Large Language Models and generate completions for these prompts. As LLMs we use 15 SOTA models, including llama3, starling-lm:7b-beta, mixtral, command r, mistral, gemma:7b, neural-chat, zephyr:7b-beta and others.

We also randomly select generation parameters for LLM during validation to make the dataset more diverse.

Data augmentation to prevent cheating
To prevent remembering Pile dataset and make it stablier to overfitting we add some augmentation to both ai-generated and human-written texts. First of all we select a random sequence of consecutive sentences from a given text. Then we add in a random place (or two) misspelling (about 10 different char-based augs) or remove a random adjective.

These augmentations don't allow miners to precalculate hashes on Pile dataset and then use them to determine whether this text is present in the human set of data or not.

Reward counting
Based on Detecting LLM-Generated Text in Computing Education article we decided to dived our reward on 3 parts:

F1 score
We decided to use it instead of classic accuracy, because it better represent quality of model especially on binary-classification tasks.

False Positive score
FP_score = 1 - FP / len(samples).

It is usually more important not to mistakenly classify human-written text as AI-generated than the other way around. It is preferable to tolerate a few more instances of student cheating or read some AI-generated emails than to wrongly penalize a real student or miss an important letter.

AP score
AP summarizes a precision-recall curve by calculating the weighted mean of precisions achieved at each threshold. This allows us to evaluate the quality of the model's ranking.

The final reward is the average of these three values.

# Vision & Roadmap

At the moment, many subnets have tasks for which they have implemented SOTA models in their miner codes to instantly achieve high quality. For such tasks, implementing better solutions could give miners only basis points of improvement. Almost no room to grow.

But our subnet is different. AI detection is a hard task to achieve high quality. That's why we aimed not just make "marketplace for inference SOTA models" as other subnets did but rather to create a constantly evolving environment where miners have to get better over time and not just run the same models for months.

In order to implement such an environment, we need to do the following.

## Validators

Currently, validators use one large dataset with human data and two models (mistral and vicuna) to generate AI texts. What could be done to improve that:

0. Use softmax on miners' scores for higher miners motivation
1. Add more models. By increasing the number and diversity of models, we will improve the overall quality of detection
2. Add more languages
3. Paraphrasing of AI texts
4. Make it resilient to tricks and attacks
5. Various types of text: differentiate articles/comments/posts/etc., in order to improve quality on each distinct type
6. Save all data that validator generates into cloud to make an open-source dataset in future

## Miners

Generally speaking, improving miners is not our task. Miners should get better themselves. But there are a few things we can do to help them:

1. Host testnet validators so miners can start without wasting TAO.
2. Make leaderboard and local dataset: we will list miners' metrics and allow people who want to start mining to evaluate their solution on a local dataset to compare them with existing ones before going to the mainnet.
3. Create Kaggle competition to introduce some of the best ML engineers to our subnet and make them run their top solution on-chain.
4. Despite the fact that solving LLM detection is a miner's problem, we are going to continue our own researches in this field to improve baseline solution and increase overall subnet's quality.
## Applications

One of the important tasks for us as subnet owners is to apply the subnet for real usage. Given the relevance of the problem, there is clearly a request for such solutions. That’s what we’re going to do:

### Web service
We’ve already developed an MVP version of a website for our subnet, where you can write some texts and then get miners' predictions with probability of this text to be ai-generated. But we’re going to develop a full version of web service, which will provide users even outside bittensor community availability to detect ai-generated texts.

### Twitter extension
Today, X/Twitter is among the top 6 social networking apps in the United States. And boasts over 500 million users worldwide. With the rapid growth of Large Language Models like ChatGpt and more and more content on the internet are generated by them. 
We’re going to build an extension for twitter, which will mark tweets and comments that you’re reading with ai-generated/human-written tags based on miners predictions from the subnet, so that people can know what content is qualitative and which texts are just auto-generated. 

### Browser extension
We also found it very useful to have an ability to instantly check whether some peace of text that you’re reading is ai-generated or human-written, so one of the application that we want to develop is a browser extension, with which users can just highlight some text and see a probability of this text to be ai-generated.

### API
As mentioned above we’re going to develop several applications based on our subnet, but there are of course many more use cases for llm-detection in particular situations/businesses. So, we are also going to provide an API service that can be used by developers for their own integrations or for making predictions on a big amount of text (for example by AI engineers to clean up their datasets).

### Commerce
All of the mentioned above services will have their own subscription plans to commercialize SN32. They will be based on api, which will be run by validators to provide access for miners and on which validators will be able to earn additional money. 

By commercializing our product, we will become less reliant on emissions and start gaining real usage. Also, by the time when dynamic tao is introduced and validators' emission becomes zero, our token will already have great utility, and validators will be earning from the mentioned services.
"""

sportstensor_roadmap = """
Introduction
Welcome to Sportstensor—the convergence of cutting-edge technology and sports data analytics. We are pioneering unprecedented innovation in sports prediction algorithms, powered by the Bittensor network.

Our Sportstensor subnet is designed to incentivize the discovery of competitive advantages over closing market odds, enabling top miners within the network to establish machine-driven dominance across the sports prediction landscape.

Why is this important?
Closing odds represent the pinnacle of market efficiency, determined by thousands of advanced machine learning algorithms.
Our subnet fosters the development of true machine intelligence by outperforming competing algorithms in a highly competitive AI-versus-AI environment.
Even with sophisticated models, bettors struggle to be profitable, as bookmakers frequently impose strict limits on consistent winners.
There is substantial demand for high-performing predictive AI from betting operators, financial firms, syndicates, and algorithmic traders seeking more accurate models.
We attract top AI and machine learning talent from diverse industries, encouraging them to revolutionize sports prediction markets.
By decentralizing the creation and improvement of predictive models, we reduce reliance on any single entity or algorithm, enhancing resilience and driving innovation in the sports prediction market.
Miner and Validator Functionality
Miner
Receives requests from the Validator containing specific information such as team names and match details.
Accesses historical data and current statistics relevant to the teams involved in the query from sports databases.
Utilizes trained machine learning models to analyze the data and predict the team they think will win and the probability.
Returns the prediction back to the Validator for confirmation and further action.
Miners must return two key pieces of information when responding to prediction requests:

probabilityChoice: The predicted outcome (Home team, Away team, Draw).
probability: The probability for that outcome, as a float between 0 and 1. e.g. 0.6 represents 60% probability.
Miners who fail to respond or provide incorrect responses will be penalized.

Validator
Match Syncing: The validator operates in an endless loop, syncing match data every 30 minutes. This includes checking upcoming, in-progress, and completed games.
League Commitment: Validators send requests every 15 minutes to acquire the active leagues a miner is committed to. Miners are required to respond with predictions for all matches in their committed leagues or receive a penalty. Miners who fail to commit to at least one league will be incrementally penalized until committing or deregistering.
Match Prediction Requests: Prediction requests are sent out at specific time intervals (24 hours, 12 hours, 4 hours, and 10 minutes before a match). Miners are penalized for non-responses.
Closing Edge Scoring: After match completion, the validator calculates the closing edge scores for each prediction and updates the local database to be used later in the scoring and weights logic.
Prediction Cleanup: Non-registered miners and outdated predictions are regularly cleaned from the system to ensure only valid data is kept.
Scoring and Weights
Incentive Mechanism:
Incentives and scores are calculated every 20 minutes in a background thread.
Each active league is iterated through to calculate scores for that league.
During each league iteration, every miner is scored for their prediction accuracy.
The max number of predictions included for a miner per league is determined by the league’s ROLLING_PREDICTION_THRESHOLD_BY_LEAGUE multiplied by 2.
This creates a constantly rolling forward set of predictions per miner per league, so older predictions outside these thresholds will not be scored.
Incentive scores are calculated through a series of complex algorithms. Please see our whitepaper for more details. Also analyze vali_utils/scoring_utils.py.
After all active leagues have been scored, league-specific scoring percentages are applied.
Final scores are aggregated and logged for weight setting.
Validators set the miners' weights on the chain based on these scores.
Roadmap
Phase 1: Foundation (Q3 2024)
 Launch on testnet (172)
 Develop baseline model for soccer (Major League Soccer)
 Develop baseline model for baseball (Major League Baseball)
 Launch website (sportstensor.com)
 Begin marketing for brand awareness and interest
 Build dashboard
 Launch front-end application
Phase 2: Upgrade (Q4 2024)
 Upgrade incentive mechanism to v2
 Upgrade dashboard to track miner performance and progress
 Achieve machine learning dominance over the sports prediction market by our top miners
 Collaborations and partnerships with synergistic companies and subnets
 Build application to monetize validator bandwidth
 Expand on commitable leagues
Phase 3: Expand (Q1 2025)
 Market and B2B sales expansion
 Grow the team
 Explore niche sports offerings
 Develop additional products
"""

chunking_roadmap = """
# What is Chunking?

Chunking is the process of breaking down a set of data into smaller, more manageable "chunks" of data. This technique is essential in natural language processing (NLP) and particularly useful when working with large language models (LLMs). Chunking can involve various methods of segmentation, such as splitting an article into sections, a screenplay into scenes, or a recording of a concerto into movements.

## Why Chunk?

For LLMs to provide accurate information, it must have access to that information. Thus, when LLMs need to access extensive knowledge beyond its training data, that information needs to be part of the request to prevent hallucinations. Due to the high cost of inference, including the entire corpus of data in every request is impractical.

We address this issue with chunking. By breaking down data into smaller chunks and transforming these chunks into vectors with embedded meanings, we store them in a vector database. When a user sends a query, we embed it as a vector and identify the vectors in the database that are most related to the query. For example, instead of loading an entire book into the model’s context, we retrieve only the relevant chunks of text, significantly reducing the total number of tokens processed per query.

Chunking, therefore, enables efficient and cost-effective querying by focusing on relevant portions of text, maintaining the balance between comprehensive knowledge and resource management.

Chunking is a crucial preliminary step for many machine learning (ML) tasks that use large amounts of data, such as:

- **Retrieval-Augmented Generation (RAG):** RAG utilizes a database of relevant documents to give LLMs the proper context to parse a particular query. Effective chunking results in more relevant and specific texts being included in the LLM’s context window, leading to better responses.

- **Classification:** Chunking can separate texts into similar sections, which can then be classified and assigned labels. This enhances the accuracy and efficiency of classification tasks.

- **Semantic Search:** Improved chunking can enhance the accuracy and reliability of semantic searching algorithms, which return results based on semantic meaning rather than simple keyword matching.
Conversational AI is Booming

39% of all B2C chats involve a chatbot.
40% of millennials interact with chatbots daily.
74% of users prefer interacting with chatbots for seeking answers to FAQs.
Entertainment and Consumer-Facing Applications Are Experiencing Explosive Growth

Many lesser-known apps, including Character AI, boast hundreds of millions of monthly visits.

ChatGPT: 2.4B
Gemini: 317M
Character.ai: 211M
JanitorAi: 41M
CivitAi: 12M
Claude: 44M
ElevenLabs: 13M
QuillBot: 65M
Liner: 20M
Poe: 30M
Perplexity: 47M
The Problem with Current Large Language Models (LLMs)

Static and Expensive to Update: LLMs are "frozen-in-time" and unaware of events post their knowledge cutoff date.
Lack Domain-Specific Knowledge: They are generalized and do not possess niche details about specific domains or private data.
Opaque Functioning: LLMs operate as "black boxes," making it unclear how they arrive at conclusions, often leading to hallucinated responses.
Inefficient and Costly: Training competitive foundation models requires immense computational resources, making it unrealistic for even large companies to create their own tailored models.
Retrieval-Augmented Generation (RAG)

RAG enables applications like ChatGPT and Cohere to utilize user-provided data and access extensive, domain-specific knowledge bases.

The RAG Pipeline

Preprocessing: Preparing data for retrieval.
Retrieval-Augmentation: For each LLM query, the pipeline includes the most relevant data from the dataset as context.
Challenges with Traditional Chunking Methods

Brute Force Approach: Traditional methods chunk data every X tokens with Y overlap, leading to redundant information. For instance, OpenAI's Assistants API chunks every 800 tokens with a 400-token overlap, resulting in 100% more redundant information.
Lack of Semantic Meaning: Arbitrary chunking "hopes" that relevant context is adjacent, which is not ideal.
Intelligent Chunking

Intelligent chunking involves sophisticated methods to segment data into meaningful, contextually relevant "chunks," often without repeating data. Common approaches include:

Semantic Chunking
Recursive Chunking
Document-Based Chunking
Agentic Chunking
VectorChat's Offerings

Toffee.ai: A user-friendly conversational AI platform built upon decentralized inference and retrieval-augmented generation.
Chunking.com: Supports intelligent chunking of various modalities, providing unmatched RAG for enterprises and developers.
Toffee.ai Features

Characters Never Forget: Through intelligent RAG, characters have effectively infinite memory, facilitating endless meaningful conversations.
Candies & Multimodality: User-defined "packs" of knowledge seamlessly enhance characters, supporting text, PDFs, images, videos, and links.
Freedom of Expression: Decentralized stack offers users maximum flexibility in interactions.
Chunking.com Features

Intelligent RAG: A front-end service for the chunking subnet, serving intelligent RAG for AI applications.
Omni-modal Support: Supports over 30 types of documents (e.g., TXT, PDF, CSV), alongside images and videos.
Industry-Leading Performance: Delivers superior performance at significantly lower costs.
Performance vs. Cost

Text-Only Zero-Shot Benchmark: Chunking.com is 2x cheaper than AI21 and 18.5% more accurate than Unstructured.
GPQA Multimodal Benchmark: Chunking.com is 128x cheaper and 30% more accurate than industry leader Unstructured in multimodal chunking.
Dataset Size: Chunking.com produces 49% fewer megabytes than LangChain, reducing downstream and runtime costs.
Why Bittensor?

Bittensor provides a straightforward, method-agnostic metric to optimize for similarity scores, incentivizing miners to fine-tune existing solutions and innovate new ones.
"""

subnet_roadmaps = {
    19: nineteen_roadmap,
    4: targon_roadmap,
    9: pretraining_roadmap,
    1: apex_roadmap,
    29: coldint_roadmap,
    13: dataverse_roadmap,
    51: compute_roadmap,
    24: omega_roadmap,
    52: prop_trading_roadmap,
    25: protein_folding_roadmap,
    11: dippy_roadmap,
    31: nas_roadmap,
    30: infinite_games_roadmap,
    21: omega_any_to_any_roadmap,
    20: bitagent_roadmap,
    37: finetuning_roadmap,
    23: socialtensor_roadmap,
    2: omron_roadmap,
    43: graphite_roadmap,
    32: itsai_roadmap,
    41: sportstensor_roadmap,
    40: chunking_roadmap,
}

# TODO: Add dynamic adapter
class StaticGithubAdapter(BaseGithubAdapter):
    def get_subnet_roadmap(self, subnet_id: int) -> str:
        if subnet_id in subnet_roadmaps:
            return subnet_roadmaps[subnet_id]
        else:
            return ""
