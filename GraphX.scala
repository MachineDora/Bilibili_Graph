import java.io.{FileWriter, PrintWriter}
import org.apache.log4j.{Level, Logger}
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.graphx.{Edge, Graph, VertexRDD}
import org.apache.spark.rdd.RDD
import org.apache.spark.graphx.VertexRDD
import scala.collection.mutable

object GraphX {

  case class VD(map:mutable.Map[Long,Int]){}
  case class ED(){}
  case class Message(){}

  def main(args: Array[String]): Unit = {

    Logger.getLogger("org.apache.spark").setLevel(Level.WARN)

    val conf = new SparkConf().setAppName("GraphXTest").setMaster("local[*]")
    val sc = new SparkContext(conf)

    val edg: RDD[String]=sc.textFile("D:\\PY\\GraphX\\Rel\\Edge2.txt")
    val tags: RDD[String] = sc.textFile("D:\\PY\\GraphX\\Rel\\Vertex.txt")

    val vertices = tags.map { line =>
      val fields = line.split(" ")
      (fields(0).toLong, fields(1))
    }

    val edges = edg.map { line =>
      val fields = line.split(" ")
      Edge(fields(0).toLong, fields(1).toLong, 1L)
    }

    val graph: Graph[String, Long] = Graph(vertices, edges)

    val ranks = graph.pageRank(0.0001).vertices

    val ranksByUsername = vertices.join(ranks).map {
      case (id, (tag, rank)) => (tag, rank)
    }.sortBy(i => i._2, false)

    val writer0 = new PrintWriter(new FileWriter("D:\\PY\\GraphX\\Rel\\pagerank.txt", true))

    //println(ranksByUsername.collect().mkString("\n"))

    //writer0.write(ranksByUsername.collect().mkString("\r\n"))

    //degree2
    val edges2 = edg.map { line =>
      val fields = line.split(" ")
      Edge[ED](fields(0).toLong, fields(1).toLong, null)
    }

    val graph2:Graph[VD, ED]=Graph.fromEdges[VD,ED](edges2,VD(mutable.Map[Long,Int]()))

    val reversalGraph=graph2.reverse

    val degreeRelation_1:VertexRDD[mutable.Map[Long, Int]]=reversalGraph.aggregateMessages[mutable.Map[Long,Int]](triplet=>{
      triplet.sendToDst(triplet.srcAttr.map.+((triplet.srcId,1)))
    },_++_)
    val degreeRelation_2:VertexRDD[mutable.Map[Long, Int]]=reversalGraph.outerJoinVertices(degreeRelation_1)((vertexId, oldVD, mapOption)
      =>mapOption.getOrElse(mutable.Map[Long,Int]())).aggregateMessages[mutable.Map[Long,Int]](triplet=>{
      val message=triplet.srcAttr.map(t=>(t._1,t._2+1)).+((triplet.srcId,1))
      triplet.sendToDst(message)
    },(m1:mutable.Map[Long,Int],m2:mutable.Map[Long,Int])=>{
      (m1/:m2){case(m,(k,v))=>m+(k->Math.min(v,m.getOrElse(k,v)))}
    })
    //graph.outerJoinVertices(degreeRelation_2)((vertexId, oldVD, mapOption) =>mapOption.getOrElse(mutable.Map[Long,Int]())).vertices.foreach(println)

    val combineGraph = reversalGraph.outerJoinVertices(degreeRelation_2)((vertexId, oldVD, mapOption) => mapOption.getOrElse(mutable.Map[Long, Int]()))

    val answerGraph = combineGraph.mapVertices {
      case (id, map) => map.retain((k, v) => v == 2)
    }

    //val writer = new PrintWriter(new FileWriter("D:\\PY\\GraphX\\Rel\\2r.txt", true))

    //answerGraph.vertices.collect.foreach(
    //v => {
    //    println(s"${v._1},${v._2}")
    //      writer.write(s"${v._1},${v._2}")
    //    writer.write("\r\n")
    //  }
    //)

  }
}
