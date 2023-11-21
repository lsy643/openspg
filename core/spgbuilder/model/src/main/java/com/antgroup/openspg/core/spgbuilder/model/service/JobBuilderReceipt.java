/*
 * Copyright 2023 Ant Group CO., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied.
 */

package com.antgroup.openspg.core.spgbuilder.model.service;

public class JobBuilderReceipt extends BaseBuilderReceipt {

  private final Long buildingJobInfoId;

  /** 如果创建的是单次调度任务，该值也会填上 */
  private final Long buildingJobInstId;

  public JobBuilderReceipt(Long buildingJobInfoId, Long buildingJobInstId) {
    super(BuilderReceiptTypeEnum.JOB);
    this.buildingJobInfoId = buildingJobInfoId;
    this.buildingJobInstId = buildingJobInstId;
  }

  public Long getBuildingJobInfoId() {
    return buildingJobInfoId;
  }

  public Long getBuildingJobInstId() {
    return buildingJobInstId;
  }
}
