package main

import (
	"encoding/binary"
	"fmt"
	"log"

	"github.com/goburrow/modbus"
)

type Modbus struct {
	Client modbus.Client
	Addr   string
}

func CreateModbus(addr string) (Modbus, error) {
	handler := modbus.NewTCPClientHandler(addr)
	err := handler.Connect()
	if err != nil {
		return Modbus{}, err
	}
	client := modbus.NewClient(handler)
	return Modbus{client, addr}, nil
}

func TestModbus(addr string, quiet bool) (bool, error) {
	handler := modbus.NewTCPClientHandler(addr)
	err := handler.Connect()
	defer handler.Close()
	client := modbus.NewClient(handler)

	results, err := client.ReadHoldingRegisters(0, 62)
	if err != nil {
		log.Printf("%v\n", err)
		return false, err
	}
	if !quiet {
		log.Printf("results %v\n", results)
	}
	return true, nil
}

func (mb *Modbus) GetCurrentPosition() (int, error) {
	results, err := mb.Client.ReadHoldingRegisters(0, 1)
	if err != nil {
		log.Printf("%v\n", err)
		return -1, err
	}
	return int(binary.BigEndian.Uint16(results)), nil
}

func (mb *Modbus) GetData(pos int) (string, error) {
	if !(pos >= 0 && pos < 7) {
		return "", fmt.Errorf("position should be between 0 and up to 7 not including")
	}
	results, err := mb.Client.ReadHoldingRegisters(uint16(pos*17+3), 17)
	if err != nil {
		log.Printf("%v\n", err)
		return "", err
	}
	return string(results), nil
}

func (mb *Modbus) GetCurrentTemperature() (int, error) {
	results, err := mb.Client.ReadHoldingRegisters(1, 1)
	if err != nil {
		log.Printf("%v\n", err)
		return -1, err
	}
	return int(binary.BigEndian.Uint16(results)), nil
}

func (mb *Modbus) GetSettedTemperature() (int, error) {
	results, err := mb.Client.ReadHoldingRegisters(2, 1)
	if err != nil {
		log.Printf("%v\n", err)
		return -1, err
	}
	return int(binary.BigEndian.Uint16(results)), nil
}

func (mb *Modbus) SetTemperature(a int) error {
	if a < 0 || a >= 65535 {
		return fmt.Errorf("Can't set temperature like this %v\n", a)
	}
	tmp := make([]byte, 2)
	binary.BigEndian.PutUint16(tmp, uint16(a))
	_, err := mb.Client.WriteMultipleRegisters(2, 1, tmp)
	return err
}

func (mb *Modbus) SetData(data string) error {
	if len(data) > 34 {
		return fmt.Errorf("Unable to parse data longer than 32 bytes: %v\n", data)
	}
	position, err := mb.GetCurrentPosition()
	if err != nil {
		log.Printf("%v\n", err)
		return err
	}
	_, err = mb.Client.WriteMultipleRegisters(uint16(position*17+3), 17, []byte(data))
	if err != nil {
		log.Printf("test %v\n", err)
		return err
	}
	mb.UpdatePosition()
	return err
}

func (mb *Modbus) UpdatePosition() error {
	pos, err := mb.GetCurrentPosition()
	if err != nil {
		log.Printf("%v\n", err)
		return err
	}
	if pos+1 == 7 {

		pos = 0
	} else {
		pos += 1
	}
	tmp := make([]byte, 2)
	binary.BigEndian.PutUint16(tmp, uint16(pos))
	mb.Client.WriteMultipleRegisters(uint16(0), uint16(1), tmp)
	return nil
}
