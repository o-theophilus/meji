<script>
	import { Switch } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import Card from './card.svelte';
	import HChart from './chart_h_bar.svelte';
	import LineChart from './chart_line.svelte';
	import Summary from './summary.svelte';
	import Table from './table.svelte';

	let sales_today = {
		value: 56909,
		prev_value: 50009
	};
	let orders_today = {
		value: 12,
		prev_value: 24
	};

	let sales_data = [
		{ month: 'Jan', sales: 120 },
		{ month: 'Feb', sales: 190 },
		{ month: 'Mar', sales: 300 },
		{ month: 'Apr', sales: 250 },
		{ month: 'May', sales: 420 },
		{ month: 'Jun', sales: 380 },
		{ month: 'Jul', sales: 450 },
		{ month: 'Aug', sales: 520 },
		{ month: 'Sep', sales: 610 },
		{ month: 'Oct', sales: 700 },
		{ month: 'Nov', sales: 850 },
		{ month: 'Dec', sales: 920 }
	];

	let revent_orders = [
		{ id: '#ORD-1024', customer: 'Mike', total: 120, status: 'Paid' },
		{ id: '#ORD-1025', customer: 'Sarah', total: 85, status: 'Pending' },
		{ id: '#ORD-1026', customer: 'David', total: 240, status: 'Paid' },
		{ id: '#ORD-1027', customer: 'Emma', total: 64, status: 'Canceled' },
		{ id: '#ORD-1028', customer: 'James', total: 150, status: 'Paid' }
	];

	let top_products = [
		{ name: 'Wireless Headphones', units: 320, revenue: 9600 },
		{ name: 'Smart Watch', units: 250, revenue: 12500 },
		{ name: 'Bluetooth Speaker', units: 210, revenue: 6300 },
		{ name: 'Gaming Mouse', units: 180, revenue: 5400 },
		{ name: 'Mechanical Keyboard', units: 150, revenue: 7500 }
	];

	let order_status = [
		{ label: 'created', count: 12 },
		{ label: 'processing', count: 8 },
		{ label: 'enroute', count: 5 },
		{ label: 'delivered', count: 20 },
		{ label: 'canceled', count: 2 }
	];

	let customers = [
		{ name: 'Mike Johnson', orders: 12, spent: 1200 },
		{ name: 'Sarah Williams', orders: 9, spent: 980 },
		{ name: 'David Brown', orders: 15, spent: 1500 },
		{ name: 'Emma Davis', orders: 7, spent: 760 },
		{ name: 'James Wilson', orders: 10, spent: 1100 }
	];

	let low_stock = [
		{ name: 'Wireless Headphones', stock: 5, reorder: 20 },
		{ name: 'Gaming Mouse', stock: 3, reorder: 15 },
		{ name: 'Bluetooth Speaker', stock: 7, reorder: 25 },
		{ name: 'Laptop Stand', stock: 4, reorder: 10 },
		{ name: 'USB-C Hub', stock: 6, reorder: 20 }
	];

	let cartData = [
		{ label: 'Abandoned', count: 3 },
		{ label: 'Checkout', count: 3 }
	];
</script>

<svelte:head>
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</svelte:head>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" />

<Content>
	<div class="page_title">Admin Dashboard</div>

	<Switch list={['Today', '1 day', '7 days', '1 month']}></Switch>

	<div class="container">
		<div class="four margin">
			<Card>
				<Summary title="Sales Today" data={sales_today} money icon="banknote"></Summary>
			</Card>
			<Card>
				<Summary title="Orders Today" data={orders_today} icon="receipt-text"></Summary>
			</Card>
			<Card>
				<Summary title="New Users Today" data={orders_today} icon="User"></Summary>
			</Card>
		</div>

		<div class="margin">
			<Card title="SALES CHART">
				<LineChart data={sales_data}></LineChart>
			</Card>
		</div>

		<div class="order_container margin">
			<Card title="RECENT ORDERS">
				<Table data={revent_orders} headers={['id', 'customer', 'total', 'status']}></Table>
			</Card>
		</div>

		<div class="margin">
			<Card title="ORDERS STATUS">
				<HChart data={order_status}></HChart>
			</Card>
		</div>

		<div class="margin">
			<Card title="Low Stock">
				<Table data={low_stock} headers={['name', 'stock']}></Table>
			</Card>
		</div>

		<div class="two margin">
			<Card title="TOP PRODUCTS">
				<Table data={top_products} headers={['name', 'units', 'revenue']}></Table>
			</Card>
			<Card title="TOP Customers">
				<Table data={customers} headers={['name', 'orders', 'spent']}></Table>
			</Card>
		</div>

		<div class="margin three">
			<Card title="Conversion Rate">
				<HChart data={cartData}></HChart>
				50%
			</Card>

			<Card title="Coupon Usage">
				Display: Columns
				<br />
				<br />
				Count | 3
				<br />
				Value | 3
			</Card>

			<Card title="Traffic / Analytics">
				Display: Columns
				<br />
				<br />
				page | 3
			</Card>
		</div>

		<br />

		<Card title="ACTIVITY FEED">
			Display: Columns
			<br />
			<br />
			New order placed | time
			<br />
			Product updated | time
			<br />
			Customer registered | time
		</Card>
	</div>
</Content>

<style>
	.container {
		container-type: inline-size;
	}

	.two {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(1, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(2, 1fr);
			}
		}
	}
	
	.three {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(1, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(3, 1fr);
			}
		}
	}

	.four {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(2, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(4, 1fr);
			}
		}
	}


	.margin {
		margin-top: 16px;
	}
</style>
