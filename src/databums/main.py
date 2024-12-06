#!/usr/bin/env python3

def main():
    import pyspark
    from pyspark.sql import SparkSession
    print(f"Hey there, i imported {SparkSession} from {pyspark}")

if __name__ == "__main__":
    main()