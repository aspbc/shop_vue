<template>
  <div class="cart-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户购物车数据大盘</span>
          <el-input
            v-model="uid"
            placeholder="按用户UID搜索"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchCarts"
            @keyup.enter="fetchCarts"
          />
          <el-button type="primary" @click="fetchCarts">搜索</el-button>
        </div>
      </template>

      <el-table :data="cartList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="购物车ID" width="100" />
        <el-table-column prop="uid" label="用户UID" width="100" />
        <el-table-column prop="productId" label="商品ID" width="100" />
        <el-table-column prop="productAttrUnique" label="商品规格编码" min-width="150" />
        <el-table-column prop="cartNum" label="商品数量" width="100" />
        <el-table-column prop="type" label="购物车类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.type === 0 ? 'info' : 'warning'">
              {{ getTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isPay" label="是否已结算" width="100">
          <template #default="{ row }">
            <el-tag :type="row.isPay === 1 ? 'success' : 'danger'">
              {{ row.isPay === 1 ? '已支付' : '未结算' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="danger" @click="handleDelete(row.id)">强制清空</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchCarts"
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

const cartList = ref([])
const loading = ref(false)
const uid = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const getTypeName = (type) => {
  const types = ['普通', '秒杀', '砍价', '拼团', '积分', '套餐']
  return types[type] || '未知'
}

const fetchCarts = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/cart/list', {
      params: { page: page.value, limit: limit.value, uid: uid.value }
    })
    if (res.data.code === 200) {
      cartList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取购物车列表失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要清理这条购物车记录吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/cart/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('清理成功')
        fetchCarts()
      }
    } catch (error) {
      ElMessage.error('清理失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchCarts()
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
