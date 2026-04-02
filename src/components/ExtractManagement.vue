<template>
  <div class="extract-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>提现申请审核</span>
          <el-select v-model="status" placeholder="审核状态" style="width: 150px; margin-left: auto; margin-right: 10px;" clearable @change="fetchExtracts">
            <el-option label="审核中" :value="0" />
            <el-option label="已提现" :value="1" />
            <el-option label="未通过" :value="-1" />
          </el-select>
          <el-button type="primary" @click="fetchExtracts">搜索</el-button>
        </div>
      </template>

      <el-table :data="extractList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="申请ID" width="80" />
        <el-table-column prop="uid" label="用户UID" width="100" />
        <el-table-column prop="realName" label="真实姓名" width="120" />
        <el-table-column prop="extractType" label="提现方式" width="100">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.extractType)">
              {{ getTypeName(row.extractType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="extractPrice" label="提现金额" width="120">
          <template #default="{ row }">
            <span style="color: red; font-weight: bold;">￥{{ row.extractPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="extractFee" label="手续费" width="100" />
        <el-table-column prop="bankCode" label="收款账号" min-width="150">
          <template #default="{ row }">
            {{ row.extractType === 'bank' ? row.bankCode : (row.extractType === 'alipay' ? row.alipayCode : '微信零钱') }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)">
              {{ getStatusName(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === 0" size="small" type="success" @click="handleAudit(row, 1)">通过</el-button>
            <el-button v-if="row.status === 0" size="small" type="danger" @click="handleAudit(row, -1)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchExtracts"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const extractList = ref([])
const loading = ref(false)
const status = ref(null)
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const getTypeName = (type) => {
  const map = { bank: '银行卡', alipay: '支付宝', wx: '微信' }
  return map[type] || type
}

const getTypeColor = (type) => {
  const map = { bank: 'warning', alipay: 'primary', wx: 'success' }
  return map[type] || 'info'
}

const getStatusName = (status) => {
  const map = { '0': '审核中', '1': '已提现', '-1': '未通过' }
  return map[status] || '未知'
}

const getStatusColor = (status) => {
  const map = { '0': 'warning', '1': 'success', '-1': 'danger' }
  return map[status] || 'info'
}

const fetchExtracts = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/finance/extract/list', {
      params: { page: page.value, limit: limit.value, status: status.value }
    })
    if (res.data.code === 200) {
      extractList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取提现列表失败')
  } finally {
    loading.value = false
  }
}

const handleAudit = (row, auditStatus) => {
  const actionName = auditStatus === 1 ? '通过' : '拒绝'
  ElMessageBox.prompt(`确定要${actionName}该提现申请吗？${auditStatus === -1 ? '请输入拒绝原因' : ''}`, '审核确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputPattern: auditStatus === -1 ? /\S+/ : null,
    inputErrorMessage: '拒绝原因不能为空'
  }).then(async ({ value }) => {
    try {
      const payload = { id: row.id, status: auditStatus }
      if (auditStatus === -1) {
        payload.failMsg = value
      }
      const res = await axios.post('/api/admin/finance/extract/audit', payload)
      if (res.data.code === 200) {
        ElMessage.success('审核处理成功')
        fetchExtracts()
      }
    } catch (error) {
      ElMessage.error('审核处理失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchExtracts()
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
}
.pagination-block {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
