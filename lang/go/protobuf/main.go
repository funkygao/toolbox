package main

import (
	"fmt"

	"github.com/funkygao/toolbox/lang/go/protobuf/demo"
	"github.com/golang/protobuf/proto"
)

func main() {
	// marshal
	msg := new(demo.DemoMsg)
	msg.ClientId = proto.Int32(8)
	msg.ClientName = proto.String("foo")
	msg.Desc = proto.String("just a demo")
	item := new(demo.MsgItem)
	item.Id = proto.Int32(55)
	item.Name = proto.String("funky")
	t := demo.ItemType(demo.ItemType_TypeY)

	item.Type = &t
	msg.Items = append(msg.Items, item)
	fmt.Println(msg.String())
	data, err := proto.Marshal(msg)
	fmt.Println(err, data)

	// unmarshal
	var pb demo.DemoMsg
	err = proto.Unmarshal(data, &pb)
	if err != nil {
		panic(err)
	}

	fmt.Println(pb.String())
}
