import sys
from pathlib import Path

from aisdecoder.message_factory import AllMessagesFactory
from aisdecoder.vdm_sentence_structure import EndsWithEpochTime
from aisdecoder.message_iterator import MessageIterator
from aisdecoder.writers.density_map import DensityMap # type: ignore
from aisdecoder.writers.writer_csv import WriterCSV
from aisdecoder.filters.filter_bbox import FilterBBox
from aisdecoder.basictypes.basic_types import Rectangle
from aisdecoder.correlate_static_iterator import CorrelateStaticIterator
from aisdecoder.sentence_error_report import sentence_error_report_singleton
from aisdecoder.writers.writer_stats import WriterStats

def file_to_csv(fn):
    with open(fn) as f:
        it = MessageIterator(
            f,
            sentence_structure = EndsWithEpochTime(),
            message_factory = AllMessagesFactory()
        )        
        for msg in it:
            print(msg.as_csv())

def file_to_netcdf(fn: Path):
    fn = Path(fn)
    #error_report_singleton.set("sentences", "input_file_size_byte", fn.stat().st_size)
    with fn.open() as f:
        it = MessageIterator(
            f,
            sentence_structure = EndsWithEpochTime(),
            message_factory = AllMessagesFactory()
        )
        map = DensityMap(
            map_boundaries=Rectangle(7, 41, 12, 45.5),
            output_file="density_map.png", 
            filters=[FilterBBox(Rectangle(7, 41, 12, 45.5))]
        )
        static_correration_it = CorrelateStaticIterator(it)
        csv = WriterCSV(Path("kine.csv"))
        stats=WriterStats(fn)
        for msg in static_correration_it:
            map.add_message(msg)
            msg.write(csv)
            msg.write(stats)
        map.generate_density_map()
        csv.close()
        #stats.save(Path("stats_msg.json"))
        stats.save(Path("~/tmp/ais_stats").expanduser().absolute()/ fn.with_suffix(".stat.json").name)


if __name__ == "__main__":
    #pprint(timeit.repeat(plain_aislib, number=1, repeat=1))
    print("------------------")
    #[9.004973700000846, 9.574930900000254, 9.082180499999595]
    if len(sys.argv) == 2:
        filepath = Path(sys.argv[1])  #-extract
    else:
        if Path("/home/giampaolo.cimino/data/ais/20250201-header.log").exists():
            filepath = Path("/home/giampaolo.cimino/data/ais/20250201-header.log").expanduser().absolute()
        else:
            filepath = Path("~/data/ais/20210919.log").expanduser().absolute()
    file_to_netcdf(filepath)
    #pprint(timeit.repeat(parse_file, number=1, repeat=1))