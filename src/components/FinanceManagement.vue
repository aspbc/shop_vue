<template>
  <div class="finance-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>财务资金流水明细</span>
          <el-input
            v-model="uid"
            placeholder="请输入用户UID检索"
            style="width: 200px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchBills"
            @keyup.enter="fetchBills"
          />
          <el-select v-model="category" placeholder="明细种类" style="width: 150px; margin-right: 10px;" clearable @change="fetchBills">
            <el-option label="余额变动" value="now_money" />
            <el-option label="积分变动" value="integral" />
            <el-option label="佣金变动" value="brokerage" />
          </el-select>
          <el-button type="primary" @click="fetchBills">搜索</el-button>
        </div>
      </template>

      <el-table :data="billList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="记录ID" width="80" />
        <el-table-column prop="uid" label="用户UID" width="100" />
        <el-table-column prop="title" label="明细标题" min-width="150" />
        <el-table-column prop="category" label="类型" width="100" />
        <el-table-column prop="pm" label="收支" width="80">
          <template #default="{ row }">
            <el-tag :type="row.pm === 1 ? 'success' : 'danger'">
              {{ row.pm === 1 ? '获得' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="number" label="变动金额/数量" width="120">
          <template #default="{ row }">
            <span :style="{ color: row.pm === 1 ? 'green' : 'red' }">
              {{ row.pm === 1 ? '+' : '-' }}{{ row.number }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="变动后剩余" width="120" />
        <el-table-column prop="mark" label="备注说明" min-width="150" show-overflow-tooltip />
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchBills"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const billList = ref([])
const loading = ref(false)
const uid = ref('')
const category = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchBills = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/finance/bill/list', {
      params: { page: page.value, limit: limit.value, uid: uid.value, category: category.value }
    })
    if (res.data.code === 200) {
      billList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取流水记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBills()
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
