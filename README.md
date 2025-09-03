# Amazon SQS Queue Setup for Order Notifications

This guide outlines the steps to set up an Amazon SQS queue and configure it to receive order change notifications from Amazon SP-API.

**Note:** Do not change anything in this setup unless you have thoroughly read and understood the documentation, or if it has been more than 6 months and the current configuration is no longer working.

**Creation Date:** 03-09-2025

**Relevant Documentation (May work in the future):**
* [Tutorial: Grant Permission to SQS Queue](https://developer-docs.amazon.com/sp-api/docs/tutorial-grant-permission-to-sqs-queue)
* [Tutorial: Subscribe to Order Change Notification](https://developer-docs.amazon.com/sp-api/docs/tutorial-subscribe-to-order-change-notification)

---

## AWS Setup

### Step 1: Prepare CloudFormation Template

We will use a CloudFormation template to create the necessary AWS resources.

1. Create a file named `orders.yml`.
2. Copy the following content into `orders.yml`

### Step 2: Login to AWS Account

Log in to your AWS Management Console.

### Step 3: Navigate to CloudFormation

1. In the AWS home page search bar, type "CloudFormation".
2. Click on "CloudFormation" from the search results.
3. Go to the "Stacks" section.

### Step 4: Create a New CloudFormation Stack

1. In the "Stacks" tab, click on "Create stack".
2. Select "With new resources (standard)".
3. Under "Prerequisite - Prepare template", select "Template is ready".
4. Under "Specify template", choose "Upload a template file".
5. Click "Choose file" and upload the `orders.yml` file you created earlier.
6. Click "Next".

### Step 5: Specify Stack Details

1. On the next page, provide a name for your stack (e.g., `SPAPI-Order-Notifications`).
2. Provide a name for your SQS queue (e.g., `MyOrderNotificationQueue`).
3. Click "Next".

### Step 6: Configure Stack Options and Review

1. On the "Configure stack options" page, keep the default options.
2. Click "Next".
3. On the "Review" page, review all the details.
4. Click "Submit".
5. Wait for the stack to be created (its status will change to `CREATE_COMPLETE`).

You have now successfully created the SQS queue!

---

## Configure SQS Queue Policy for Notifications

Now, we will modify the SQS queue policy to allow Amazon to send notifications.

### Step 1: Get SQS Queue ARN

1. In the AWS home page search bar, type "Simple Queue Service" (or "SQS").
2. Click on "Simple Queue Service" from the search results.
3. On the Amazon SQS page, you will see the name of the SQS queue you created earlier.
4. Click on your queue's name.
5. On the queue details page, look for the "ARN" value and copy it. You will use this later.

### Step 2: Edit Queue Policy

1. While still on your SQS queue's details page, click on the "Access policy" tab.
2. In the "Access policy" section, click the "Edit" button on the right side.
3. Scroll down to the "Access policy" text area and click on "Policy generator". This will open a new window or tab.
4. In the Policy Generator:
    * **Step 1:** Select "SQS Queue Policy".
    * **Step 2:**
        * Set "Effect" to "Allow".
        * Set "Principal" to `437568002678`.
        * Set "Actions" to `SendMessage` and `GetQueueAttributes`.
        * Enter the SQS ARN value (that you copied from Step 1 of this section) in the "Amazon Resource Name (ARN)" field.
    * Choose "Add Statement" and verify the details.
5. Click on "Generate Policy".
6. Copy the generated policy (JSON format).
7. Navigate back to your SQS queue's access policy page (where you clicked "Policy generator").
8. Paste the copied policy (JSON) into the "Access policy" text area, replacing any existing content if present.
9. Click "Save".

You can now receive notifications from Amazon! The AWS part is complete.

---

## Script Setup

This section details the setup for your Python scripts.

**Question:** Which region is this for? (eu or fe or ne)
Based on your region, you will need to change the URLs in your scripts accordingly.

### .env File Configuration

Your `.env` file should contain the following variables:
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
refresh_token = "YOUR_REFRESH_TOKEN"
client = "YOUR_CLIENT_IDENTIFIER" # Or specific marketplace client string
AWS_SQS_ARN = "YOUR_SQS_QUEUE_ARN" # The ARN you copied earlier
DESTINATION_ID = "" # This will be obtained after running destinationId.py


### Required Files

You will need the following Python files:

*   `order_notification.py`
*   `destinationId.py`
*   `access_token.py`
*   `access_token_for_dest.py`

### Script Execution Order

1.  **Run `destinationId.py` first.** This script will output a `DESTINATION_ID`.
2.  Take the `DESTINATION_ID` from the output and add it to your `.env` file.
3.  **Then, run `order_notification.py`.**