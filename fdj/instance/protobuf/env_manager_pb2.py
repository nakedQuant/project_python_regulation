# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: env_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="env_manager.proto",
    package="manager",
    syntax="proto3",
    serialized_options=b"Z5github.com/VegeWong/EnvManager-Go/protobuf/envmanager",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x11\x65nv_manager.proto\x12\x07manager"\t\n\x07Request"\x17\n\x05Reply\x12\x0e\n\x06status\x18\x01 \x01(\x08"2\n\tEnvConfig\x12\x10\n\x08map_name\x18\x01 \x01(\t\x12\x13\n\x0bnum_threads\x18\x02 \x01(\x03"A\n\tEnvSchema\x12\x0f\n\x07\x62\x61se_id\x18\x01 \x01(\x03\x12#\n\x07\x63onfigs\x18\x02 \x03(\x0b\x32\x12.manager.EnvConfig"-\n\x0b\x43reateReply\x12\x0e\n\x06\x65nd_id\x18\x01 \x01(\x03\x12\x0e\n\x06status\x18\x02 \x01(\x03"G\n\x05\x41rray\x12\x0e\n\x06nbytes\x18\x01 \x01(\x03\x12\r\n\x05\x64type\x18\x02 \x01(\x03\x12\x0e\n\x06shapes\x18\x03 \x03(\x03\x12\x0f\n\x07ndarray\x18\x04 \x01(\x0c"i\n\x08\x45nvArray\x12\x0e\n\x06\x65nv_id\x18\x01 \x01(\x03\x12\x12\n\ntime_steps\x18\x02 \x01(\x03\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x0c\n\x04\x64one\x18\x04 \x01(\x08\x12\x1d\n\x05\x61rray\x18\x05 \x03(\x0b\x32\x0e.manager.Array"2\n\rAgentDecision\x12!\n\x06\x61\x63tion\x18\x01 \x01(\x0b\x32\x11.manager.EnvArray"-\n\x08\x45nvReply\x12!\n\x06\x63olumn\x18\x01 \x01(\x0b\x32\x11.manager.EnvArray"2\n\x0cResetRequest\x12"\n\x07request\x18\x01 \x01(\x0b\x32\x11.manager.EnvArray"!\n\x0c\x43loseRequest\x12\x11\n\tclose_ids\x18\x01 \x03(\x03"0\n\nCloseReply\x12\x12\n\nclosed_ids\x18\x01 \x03(\x03\x12\x0e\n\x06status\x18\x02 \x01(\x08"P\n\x10\x42lockDescription\x12\x16\n\x0emax_block_size\x18\x01 \x01(\x03\x12\x16\n\x0emin_block_size\x18\x02 \x01(\x03\x12\x0c\n\x04mode\x18\x03 \x01(\x03"L\n\nBlockReply\x12\r\n\x05ready\x18\x01 \x01(\x08\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x08\x12"\n\x07\x63olumns\x18\x03 \x03(\x0b\x32\x11.manager.EnvArray2\x97\x02\n\x0c\x45nvManageRPC\x12)\n\x05\x43heck\x12\x10.manager.Request\x1a\x0e.manager.Reply\x12\x35\n\tCreateEnv\x12\x12.manager.EnvSchema\x1a\x14.manager.CreateReply\x12\x38\n\x08ResetEnv\x12\x15.manager.ResetRequest\x1a\x11.manager.EnvReply(\x01\x30\x01\x12\x38\n\x07StepEnv\x12\x16.manager.AgentDecision\x1a\x11.manager.EnvReply(\x01\x30\x01\x12\x31\n\x08\x43loseEnv\x12\x10.manager.Request\x1a\x13.manager.CloseReply2y\n\nDataBuffer\x12\x39\n\x07Request\x12\x19.manager.BlockDescription\x1a\x13.manager.BlockReply\x12\x30\n\x04Step\x12\x16.manager.AgentDecision\x1a\x0e.manager.Reply(\x01\x42\x37Z5github.com/VegeWong/EnvManager-Go/protobuf/envmanagerb\x06proto3',
)


_REQUEST = _descriptor.Descriptor(
    name="Request",
    full_name="manager.Request",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=30,
    serialized_end=39,
)


_REPLY = _descriptor.Descriptor(
    name="Reply",
    full_name="manager.Reply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="status",
            full_name="manager.Reply.status",
            index=0,
            number=1,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=41,
    serialized_end=64,
)


_ENVCONFIG = _descriptor.Descriptor(
    name="EnvConfig",
    full_name="manager.EnvConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="map_name",
            full_name="manager.EnvConfig.map_name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="num_threads",
            full_name="manager.EnvConfig.num_threads",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=66,
    serialized_end=116,
)


_ENVSCHEMA = _descriptor.Descriptor(
    name="EnvSchema",
    full_name="manager.EnvSchema",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="base_id",
            full_name="manager.EnvSchema.base_id",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="configs",
            full_name="manager.EnvSchema.configs",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=118,
    serialized_end=183,
)


_CREATEREPLY = _descriptor.Descriptor(
    name="CreateReply",
    full_name="manager.CreateReply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="end_id",
            full_name="manager.CreateReply.end_id",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="status",
            full_name="manager.CreateReply.status",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=185,
    serialized_end=230,
)


_ARRAY = _descriptor.Descriptor(
    name="Array",
    full_name="manager.Array",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="nbytes",
            full_name="manager.Array.nbytes",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="dtype",
            full_name="manager.Array.dtype",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="shapes",
            full_name="manager.Array.shapes",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="ndarray",
            full_name="manager.Array.ndarray",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=232,
    serialized_end=303,
)


_ENVARRAY = _descriptor.Descriptor(
    name="EnvArray",
    full_name="manager.EnvArray",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="env_id",
            full_name="manager.EnvArray.env_id",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="time_steps",
            full_name="manager.EnvArray.time_steps",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="type",
            full_name="manager.EnvArray.type",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="done",
            full_name="manager.EnvArray.done",
            index=3,
            number=4,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="array",
            full_name="manager.EnvArray.array",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=305,
    serialized_end=410,
)


_AGENTDECISION = _descriptor.Descriptor(
    name="AgentDecision",
    full_name="manager.AgentDecision",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="action",
            full_name="manager.AgentDecision.action",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=412,
    serialized_end=462,
)


_ENVREPLY = _descriptor.Descriptor(
    name="EnvReply",
    full_name="manager.EnvReply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="column",
            full_name="manager.EnvReply.column",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=464,
    serialized_end=509,
)


_RESETREQUEST = _descriptor.Descriptor(
    name="ResetRequest",
    full_name="manager.ResetRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="request",
            full_name="manager.ResetRequest.request",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=511,
    serialized_end=561,
)


_CLOSEREQUEST = _descriptor.Descriptor(
    name="CloseRequest",
    full_name="manager.CloseRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="close_ids",
            full_name="manager.CloseRequest.close_ids",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=563,
    serialized_end=596,
)


_CLOSEREPLY = _descriptor.Descriptor(
    name="CloseReply",
    full_name="manager.CloseReply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="closed_ids",
            full_name="manager.CloseReply.closed_ids",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="status",
            full_name="manager.CloseReply.status",
            index=1,
            number=2,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=598,
    serialized_end=646,
)


_BLOCKDESCRIPTION = _descriptor.Descriptor(
    name="BlockDescription",
    full_name="manager.BlockDescription",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="max_block_size",
            full_name="manager.BlockDescription.max_block_size",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="min_block_size",
            full_name="manager.BlockDescription.min_block_size",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="mode",
            full_name="manager.BlockDescription.mode",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=648,
    serialized_end=728,
)


_BLOCKREPLY = _descriptor.Descriptor(
    name="BlockReply",
    full_name="manager.BlockReply",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="ready",
            full_name="manager.BlockReply.ready",
            index=0,
            number=1,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="end",
            full_name="manager.BlockReply.end",
            index=1,
            number=2,
            type=8,
            cpp_type=7,
            label=1,
            has_default_value=False,
            default_value=False,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="columns",
            full_name="manager.BlockReply.columns",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=730,
    serialized_end=806,
)

_ENVSCHEMA.fields_by_name["configs"].message_type = _ENVCONFIG
_ENVARRAY.fields_by_name["array"].message_type = _ARRAY
_AGENTDECISION.fields_by_name["action"].message_type = _ENVARRAY
_ENVREPLY.fields_by_name["column"].message_type = _ENVARRAY
_RESETREQUEST.fields_by_name["request"].message_type = _ENVARRAY
_BLOCKREPLY.fields_by_name["columns"].message_type = _ENVARRAY
DESCRIPTOR.message_types_by_name["Request"] = _REQUEST
DESCRIPTOR.message_types_by_name["Reply"] = _REPLY
DESCRIPTOR.message_types_by_name["EnvConfig"] = _ENVCONFIG
DESCRIPTOR.message_types_by_name["EnvSchema"] = _ENVSCHEMA
DESCRIPTOR.message_types_by_name["CreateReply"] = _CREATEREPLY
DESCRIPTOR.message_types_by_name["Array"] = _ARRAY
DESCRIPTOR.message_types_by_name["EnvArray"] = _ENVARRAY
DESCRIPTOR.message_types_by_name["AgentDecision"] = _AGENTDECISION
DESCRIPTOR.message_types_by_name["EnvReply"] = _ENVREPLY
DESCRIPTOR.message_types_by_name["ResetRequest"] = _RESETREQUEST
DESCRIPTOR.message_types_by_name["CloseRequest"] = _CLOSEREQUEST
DESCRIPTOR.message_types_by_name["CloseReply"] = _CLOSEREPLY
DESCRIPTOR.message_types_by_name["BlockDescription"] = _BLOCKDESCRIPTION
DESCRIPTOR.message_types_by_name["BlockReply"] = _BLOCKREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType(
    "Request",
    (_message.Message,),
    {
        "DESCRIPTOR": _REQUEST,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.Request)
    },
)
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType(
    "Reply",
    (_message.Message,),
    {
        "DESCRIPTOR": _REPLY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.Reply)
    },
)
_sym_db.RegisterMessage(Reply)

EnvConfig = _reflection.GeneratedProtocolMessageType(
    "EnvConfig",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENVCONFIG,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.EnvConfig)
    },
)
_sym_db.RegisterMessage(EnvConfig)

EnvSchema = _reflection.GeneratedProtocolMessageType(
    "EnvSchema",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENVSCHEMA,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.EnvSchema)
    },
)
_sym_db.RegisterMessage(EnvSchema)

CreateReply = _reflection.GeneratedProtocolMessageType(
    "CreateReply",
    (_message.Message,),
    {
        "DESCRIPTOR": _CREATEREPLY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.CreateReply)
    },
)
_sym_db.RegisterMessage(CreateReply)

Array = _reflection.GeneratedProtocolMessageType(
    "Array",
    (_message.Message,),
    {
        "DESCRIPTOR": _ARRAY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.Array)
    },
)
_sym_db.RegisterMessage(Array)

EnvArray = _reflection.GeneratedProtocolMessageType(
    "EnvArray",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENVARRAY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.EnvArray)
    },
)
_sym_db.RegisterMessage(EnvArray)

AgentDecision = _reflection.GeneratedProtocolMessageType(
    "AgentDecision",
    (_message.Message,),
    {
        "DESCRIPTOR": _AGENTDECISION,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.AgentDecision)
    },
)
_sym_db.RegisterMessage(AgentDecision)

EnvReply = _reflection.GeneratedProtocolMessageType(
    "EnvReply",
    (_message.Message,),
    {
        "DESCRIPTOR": _ENVREPLY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.EnvReply)
    },
)
_sym_db.RegisterMessage(EnvReply)

ResetRequest = _reflection.GeneratedProtocolMessageType(
    "ResetRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESETREQUEST,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.ResetRequest)
    },
)
_sym_db.RegisterMessage(ResetRequest)

CloseRequest = _reflection.GeneratedProtocolMessageType(
    "CloseRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _CLOSEREQUEST,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.CloseRequest)
    },
)
_sym_db.RegisterMessage(CloseRequest)

CloseReply = _reflection.GeneratedProtocolMessageType(
    "CloseReply",
    (_message.Message,),
    {
        "DESCRIPTOR": _CLOSEREPLY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.CloseReply)
    },
)
_sym_db.RegisterMessage(CloseReply)

BlockDescription = _reflection.GeneratedProtocolMessageType(
    "BlockDescription",
    (_message.Message,),
    {
        "DESCRIPTOR": _BLOCKDESCRIPTION,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.BlockDescription)
    },
)
_sym_db.RegisterMessage(BlockDescription)

BlockReply = _reflection.GeneratedProtocolMessageType(
    "BlockReply",
    (_message.Message,),
    {
        "DESCRIPTOR": _BLOCKREPLY,
        "__module__": "env_manager_pb2"
        # @@protoc_insertion_point(class_scope:manager.BlockReply)
    },
)
_sym_db.RegisterMessage(BlockReply)


DESCRIPTOR._options = None

_ENVMANAGERPC = _descriptor.ServiceDescriptor(
    name="EnvManageRPC",
    full_name="manager.EnvManageRPC",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=809,
    serialized_end=1088,
    methods=[
        _descriptor.MethodDescriptor(
            name="Check",
            full_name="manager.EnvManageRPC.Check",
            index=0,
            containing_service=None,
            input_type=_REQUEST,
            output_type=_REPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name="CreateEnv",
            full_name="manager.EnvManageRPC.CreateEnv",
            index=1,
            containing_service=None,
            input_type=_ENVSCHEMA,
            output_type=_CREATEREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name="ResetEnv",
            full_name="manager.EnvManageRPC.ResetEnv",
            index=2,
            containing_service=None,
            input_type=_RESETREQUEST,
            output_type=_ENVREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name="StepEnv",
            full_name="manager.EnvManageRPC.StepEnv",
            index=3,
            containing_service=None,
            input_type=_AGENTDECISION,
            output_type=_ENVREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name="CloseEnv",
            full_name="manager.EnvManageRPC.CloseEnv",
            index=4,
            containing_service=None,
            input_type=_REQUEST,
            output_type=_CLOSEREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_ENVMANAGERPC)

DESCRIPTOR.services_by_name["EnvManageRPC"] = _ENVMANAGERPC


_DATABUFFER = _descriptor.ServiceDescriptor(
    name="DataBuffer",
    full_name="manager.DataBuffer",
    file=DESCRIPTOR,
    index=1,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=1090,
    serialized_end=1211,
    methods=[
        _descriptor.MethodDescriptor(
            name="Request",
            full_name="manager.DataBuffer.Request",
            index=0,
            containing_service=None,
            input_type=_BLOCKDESCRIPTION,
            output_type=_BLOCKREPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.MethodDescriptor(
            name="Step",
            full_name="manager.DataBuffer.Step",
            index=1,
            containing_service=None,
            input_type=_AGENTDECISION,
            output_type=_REPLY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_DATABUFFER)

DESCRIPTOR.services_by_name["DataBuffer"] = _DATABUFFER

# @@protoc_insertion_point(module_scope)
