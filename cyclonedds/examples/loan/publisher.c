#include "dds/dds.h"
#include "HelloWorldData.h"
#include "dds/ddsc/dds_public_loan_api.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    dds_entity_t participant;
    dds_entity_t topic;
    dds_entity_t writer;
    dds_return_t rc;
    uint32_t status = 0;

    participant = dds_create_participant(DDS_DOMAIN_DEFAULT, NULL, NULL);
    topic = dds_create_topic(
        participant, &HelloWorldData_Msg_desc, "HelloWorldData_Msg", NULL, NULL);
    writer = dds_create_writer(participant, topic, NULL, NULL);
    dds_set_status_mask(writer, DDS_PUBLICATION_MATCHED_STATUS);

    printf("=== [Publisher] Waiting for reader...\n");
    fflush(stdout);

    while (!(status & DDS_PUBLICATION_MATCHED_STATUS)) {
        dds_get_status_changes(writer, &status);
        dds_sleepfor(DDS_MSECS(20));
    }

    printf("=== [Publisher] Requesting loan...\n");

    void *sample = NULL;
    rc = dds_request_loan(writer, &sample);

    if (rc != DDS_RETCODE_OK) {
        printf("Failed to get loan: %s\n", dds_strretcode(-rc));
        return EXIT_FAILURE;
    }

    HelloWorldData_Msg *msg = (HelloWorldData_Msg *)sample;

    msg->userID = 1;
    msg->message = "你好，loan世界12435";

    printf("=== [Publisher]  Writing: (%d, %s)\n", msg->userID, msg->message);

    rc = dds_write(writer, msg);

    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_write: %s\n", dds_strretcode(-rc));

    dds_delete(participant);
    return EXIT_SUCCESS;
}
