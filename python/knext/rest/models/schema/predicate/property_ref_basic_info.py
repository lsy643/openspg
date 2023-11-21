# coding: utf-8

"""
    knext

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

#  Copyright 2023 Ant Group CO., Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
#  in compliance with the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied.

import pprint
import re  # noqa: F401

import six

from knext.rest.configuration import Configuration


class PropertyRefBasicInfo(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "name": "PredicateIdentifier",
        "name_zh": "str",
        "desc": "str",
        "creator": "str",
    }

    attribute_map = {
        "name": "name",
        "name_zh": "nameZh",
        "desc": "desc",
        "creator": "creator",
    }

    def __init__(
        self,
        name=None,
        name_zh=None,
        desc=None,
        creator=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """PropertyRefBasicInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._name_zh = None
        self._desc = None
        self._creator = None
        self.discriminator = None

        self.name = name
        if name_zh is not None:
            self.name_zh = name_zh
        if desc is not None:
            self.desc = desc
        if creator is not None:
            self.creator = creator

    @property
    def name(self):
        """Gets the name of this PropertyRefBasicInfo.  # noqa: E501


        :return: The name of this PropertyRefBasicInfo.  # noqa: E501
        :rtype: PredicateIdentifier
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PropertyRefBasicInfo.


        :param name: The name of this PropertyRefBasicInfo.  # noqa: E501
        :type: PredicateIdentifier
        """
        if (
            self.local_vars_configuration.client_side_validation and name is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def name_zh(self):
        """Gets the name_zh of this PropertyRefBasicInfo.  # noqa: E501


        :return: The name_zh of this PropertyRefBasicInfo.  # noqa: E501
        :rtype: str
        """
        return self._name_zh

    @name_zh.setter
    def name_zh(self, name_zh):
        """Sets the name_zh of this PropertyRefBasicInfo.


        :param name_zh: The name_zh of this PropertyRefBasicInfo.  # noqa: E501
        :type: str
        """

        self._name_zh = name_zh

    @property
    def desc(self):
        """Gets the desc of this PropertyRefBasicInfo.  # noqa: E501


        :return: The desc of this PropertyRefBasicInfo.  # noqa: E501
        :rtype: str
        """
        return self._desc

    @desc.setter
    def desc(self, desc):
        """Sets the desc of this PropertyRefBasicInfo.


        :param desc: The desc of this PropertyRefBasicInfo.  # noqa: E501
        :type: str
        """

        self._desc = desc

    @property
    def creator(self):
        """Gets the creator of this PropertyRefBasicInfo.  # noqa: E501


        :return: The creator of this PropertyRefBasicInfo.  # noqa: E501
        :rtype: str
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this PropertyRefBasicInfo.


        :param creator: The creator of this PropertyRefBasicInfo.  # noqa: E501
        :type: str
        """

        self._creator = creator

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PropertyRefBasicInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PropertyRefBasicInfo):
            return True

        return self.to_dict() != other.to_dict()
