<template>
  <div>
    <el-card>
            <el-form :inline="true" class="demo-form-inline" size="default">
        <el-form-item label="关键字：">
          <el-input v-model="searchQuery.keyword" placeholder="订单号/用户昵称" clearable style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item label="收支类型：">
          <el-select v-model="searchQuery.pm" placeholder="全部" clearable style="width: 150px;">
            <el-option label="收入" value="1"></el-option>
            <el-option label="支出" value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
      </el-form>
            <div style="margin-bottom: 15px;">
        <el-button type="warning" @click="handleExport">导出资金流水</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="order_id" label="关联单号" width="180" align="center" />
        <el-table-column prop="user_info" label="用户信息" min-width="150" align="center">
          <template #default="scope">
            <div style="font-size: 13px;">{{ scope.row.nickname }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="pm" label="收支类型" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.pm === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.pm === 1 ? '收入' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="number" label="金额" width="120" align="center">
          <template #default="scope">
            <span :style="{ color: scope.row.pm === 1 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
              {{ scope.row.pm === 1 ? '+' : '-' }}{{ scope.row.number }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="明细类型" width="120" align="center" />
        <el-table-column prop="mark" label="备注" min-width="200" show-overflow-tooltip />
        <el-table-column prop="create_time" label="发生时间" width="160" align="center" />
      </el-table>
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="total" />
      </div>
    </el-card>

    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form label-width="100px" :model="form" ref="formRef">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="请输入名称"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="form.remark" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="资金流水详情" v-model="detailVisible" width="500px">
      <el-descriptions border :column="1">
        <el-descriptions-item label="ID">{{ detailData.id }}</el-descriptions-item>
        <el-descriptions-item label="名称">{{ detailData.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailData.status === 1 ? 'success' : 'danger'">{{ detailData.status === 1 ? '启用' : '禁用' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailData.createTime }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ detailData.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const axios = inject('axios')
const tableData = ref([])
const total = ref(0)
const loading = ref(false)

const dialogVisible = ref(false)
const dialogTitle = ref('新增')
const detailVisible = ref(false)
const detailData = ref({})
const selectedRows = ref([])

const searchQuery = reactive({
  keyword: ''
})

const form = reactive({
  id: null,
  name: '',
  status: 1,
  remark: ''
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/extend/statistic_capital/list', { params: searchQuery })
    if (res.data.code === 200) {
      tableData.value = res.data.data.records || res.data.data
      total.value = res.data.data.total || res.data.data.length
    } else {
      ElMessage.error(res.data.msg || '获取数据失败')
    }
  } catch (error) {
    if (!error.response || error.response.status !== 401) {
      ElMessage.error('获取列表失败')
    }
  } finally {
    loading.value = false
  }
}

const resetData = () => {
  searchQuery.keyword = ''
  fetchData()
}

const handleSelectionChange = (val) => {
  selectedRows.value = val
}

const handleAdd = () => {
  dialogTitle.value = '添加资金流水'
  form.id = null
  form.name = ''
  form.status = 1
  form.remark = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑资金流水'
  form.id = row.id
  form.name = row.name
  form.status = row.status
  form.remark = row.remark || ''
  dialogVisible.value = true
}

const handleDetail = async (row) => {
  try {
    const res = await axios.get(`/api/admin/extend/statistic_capital/detail?id=${row.id}`)
    if (res.data.code === 200) {
      detailData.value = res.data.data
    } else {
      detailData.value = { ...row }
    }
  } catch(e) {
    detailData.value = { ...row }
  }
  detailVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    const res = await axios.post(`/api/admin/extend/statistic_capital/save`, row)
    if (res.data.code === 200) {
      ElMessage.success('状态修改成功')
    } else {
      ElMessage.error(res.data.msg || '状态修改失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      const res = await axios.post(`/api/admin/extend/statistic_capital/delete`, { id: row.id })
      if (res.data.code === 200) {
        ElMessage.success(res.data.msg || '删除成功')
        fetchData()
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) {
    return ElMessage.warning('请选择要删除的数据')
  }
  ElMessageBox.confirm(`确认删除选中的 ${selectedRows.value.length} 条记录吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    const ids = selectedRows.value.map(item => item.id)
    try {
      const res = await axios.post(`/api/admin/extend/statistic_capital/delete`, { ids })
      if (res.data.code === 200) {
        ElMessage.success('批量删除成功')
        fetchData()
      } else {
        ElMessage.error(res.data.msg || '删除失败')
      }
    } catch(e) {
      ElMessage.error('网络错误')
    }
  }).catch(() => {})
}

const handleExport = async () => {
  ElMessage.success('开始导出数据...')
  try {
    const res = await axios.get(`/api/admin/extend/statistic_capital/export`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', '资金流水_export.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch(e) {
    ElMessage.error('导出失败')
  }
}

const submitForm = async () => {
  try {
    const res = await axios.post(`/api/admin/extend/statistic_capital/save`, form)
    if (res.data.code === 200) {
      ElMessage.success(res.data.msg || '保存成功')
      dialogVisible.value = false
      fetchData()
    } else {
      ElMessage.error(res.data.msg || '保存失败')
    }
  } catch(e) {
    ElMessage.error('网络错误')
  }
}

onMounted(() => {
  fetchData()
})
</script>
