<template>
  <div class="main">
    <div>
      <el-row>
        存储：
        <el-select v-model="driveName" @change="getFileList">
          <el-option v-for="item in storageList"
                     :key="item"
                     :label="item"
                     :value="item">
          </el-option>
        </el-select>
      </el-row>
    </div>

    <div style="margin: 20px">
      <el-table
          :data="dataList"
          style="width: 100%"
          @cell-click="openChildDir"
          :default-sort="{prop: 'size', order: 'descending'}"
      >
        <el-table-column
            align="left"
            prop="name"
            label="文件"
            sortable
            width="800">
          <template slot-scope="scope">
            <template v-if="scope.row.dirFlag === true">
              <img style="width: 15px" src="./../assets/dir.svg"/>
            </template>
            <b style="margin-left: 15px">
              {{ scope.row.name }}
            </b>
          </template>

        </el-table-column>
        <el-table-column
            prop="size"
            label="大小"
            sortable
            width="250">
        </el-table-column>
        <el-table-column
            prop="date"
            label="时间">
        </el-table-column>

        <el-table-column
            fixed="right"
            label="操作"
            width="100">
          <template slot-scope="scope">
            <el-button @click="look(scope.row)" type="text" size="small">查看</el-button>
            <el-button type="text" size="small" @click="delete(scope.row)">删除</el-button>
          </template>
        </el-table-column>

      </el-table>

      <el-pagination
          @current-change="handleCurrentChange"
          background
          :current-page.sync="currentPage"
          :page-size="pageSize"
          layout="prev, pager, next"
          :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Main',
  data() {
    return {
      dataList: [],
      driveName: '',
      prefix: '',
      storageList: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
    }
  },
  created() {
    this.getDriveList()
  },
  methods: {
    getDriveList() {
      this.$axios('https://www.hexianwei.com/cloud/storages').then(res => {
        this.storageList = res.data
        this.driveName = this.storageList[0]
        this.getFileList()
      })
    },
    getFileList() {
      this.$axios('https://www.hexianwei.com/cloud/list?prefix=' + this.prefix + '&storage=' + this.driveName + '&page=' + this.currentPage + '&pageSize=20').then(res => {
        this.dataList = res.data.data
        this.currentPage = res.data.page
        this.pageSize = res.data.pageSize
        this.total = res.data.total
      })
    },
    look(row) {
      console.log(row.name)
    },
    delete(row) {
      console.log(row)
    },
    handleCurrentChange() {
      this.getFileList()
    },
    openChildDir(row, column, cell, event) {
      this.prefix = this.prefix + '/' + row.name
      console.log(this.prefix)
      console.log(column)
      console.log(cell)
      console.log(event)
      this.getFileList()
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
