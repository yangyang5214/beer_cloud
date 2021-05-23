<template>
  <div class="main">
    <el-row>
      存储：
      <el-select v-model="currentStorage" @change="getFileList">
        <el-option v-for="item in storageList"
                   :key="item.name"
                   :label="item.name"
                   :value="item.name">
        </el-option>
      </el-select>
    </el-row>

    <el-row style="margin-left: 50px">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item
            @click.native="directGo(-1)"
        >
          Home
        </el-breadcrumb-item>
        <el-breadcrumb-item
            v-for="(sub, index) in prefix.split('/')"
            :key="sub"
            @click.native="directGo(index)"
        >
          {{ sub }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </el-row>

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
            <el-button type="text" size="small" @click="deleteFile(scope.row)">删除</el-button>
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
      currentStorage: '',
      prefix: '',
      storageList: [],
      currentPage: 1,
      pageSize: 20,
      total: 0,
    }
  },
  created() {
    this.getStorageList()
  },
  methods: {
    getStorageList() {
      this.$axios('storages').then(res => {
        this.storageList = res.data
        this.currentStorage = this.storageList[0]
        this.getFileList()
      })
    },
    getFileList() {
      this.$axios('list?prefix=' + this.prefix + '&storage=' + this.currentStorage.name + '&page=' + this.currentPage + '&pageSize=20').then(res => {
        this.dataList = res.data.data
        this.currentPage = res.data.page
        this.pageSize = res.data.pageSize
        this.total = res.data.total
      })
    },
    look(row) {
      let finalUrl = this.currentStorage.url + '/' + this.prefix + '/' + row.name
      window.open(finalUrl, '_blank');
    },
    directGo(index) {
      if (index === -1) {
        this.prefix = ''
      } else {
        this.prefix = this.prefix.split('/').slice(0, index + 1).join('/')
      }
      this.getFileList()
    },
    deleteFile(row) {
      let fileName = this.prefix + '/' + row.name
      console.log(fileName)
      this.$axios('del?prefix=' + fileName + '&storage=' + this.currentStorage.name).then(res => {
        console.log(res)
        this.getFileList()
      })
    },
    handleCurrentChange() {
      this.getFileList()
    },
    openChildDir(row, column) {
      if (column.property !== 'name') {
        return
      }
      if (row.dirFlag) {
        if (this.prefix === '') {
          this.prefix = row.name
        } else {
          this.prefix = this.prefix + '/' + row.name
        }
        this.getFileList()
      } else {
        this.look(row)
      }
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
