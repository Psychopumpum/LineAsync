package main

import (
    "fmt"
    "flag"
    "os"
    "./go-qrcode"
)
func usage() {
    fmt.Fprintf(os.Stderr, "usage: %s [inputfile]\n", os.Args[0])
    flag.PrintDefaults()
    os.Exit(2)
}

func main() {
    flag.Usage = usage
    flag.Parse()

    args := flag.Args()
    if len(args) < 1 {
        fmt.Println("Url missing");
        os.Exit(1);
    }
    callbackUrl := args[0]
    encodedQR, err := qrcode.New(callbackUrl, qrcode.Medium)
    if err != nil {
        fmt.Println("failed to encode QR code: %w", err)
    }
    qrString := encodedQR.ToSmallString(false)
    fmt.Println(qrString)
}