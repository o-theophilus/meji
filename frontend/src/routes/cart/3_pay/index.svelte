<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';

	import { app, loading, notify } from '$lib/store.svelte.js';
	import { Content } from '$lib/layout';
	import { IG } from '$lib/input';
	import { Button, RoundButton } from '$lib/button';
	import { Datetime } from '$lib/macro';
	import Pay from './pay.svelte';
	import Receiver from '../../orders/[slug]/_receiver.svelte';
	import Table from '../../orders/[slug]/_items_table.svelte';

	let { ops = $bindable() } = $props();
	let form = $state({
		name: ops.cart.delivery_date || ''
	});
	let error = $state({});
	let total = $derived.by(() => {
		let temp = 0;
		for (const i of app.cart_items) {
			temp += i.price * i.quantity;
		}
		return temp;
	});

	const today = new Date();
	const nextWeek = new Date(today);
	nextWeek.setDate(today.getDate() + 7);

	const validate = () => {
		// Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/delivery_date`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();
		console.log(resp);

		if (resp.status == 200) {
			notify.open('Delivery Date Saved');
			ops.cart = resp.cart;
			ops.status = 'payment';
		} else {
			error = resp;
		}
	};
</script>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	<div class="line">
		<RoundButton
			icon="arrow-left"
			onclick={() => {
				ops.status = 'receiver';
			}}
		></RoundButton>
		<div class="page_title">Summary</div>
	</div>

	<div class="card">
		<Table items={app.cart_items} />
		<br />
		<div class="line space">
			<span class="label bold"> Total Item Cost: </span>
			<span class="cost">
				₦{total.toLocaleString()}
			</span>
		</div>

		<hr class="hr" />

		<span class="label bold">To be delivered to:</span>
		<br /><br />
		<Receiver receiver={ops.cart.receiver} />

		<hr class="hr" />

		<span class="label bold"> Delivery Date: </span>
		<span class="label">
			<Datetime datetime={nextWeek} type="date_numeric" />
		</span>
		<!-- {ops.cart.delivery_date} -->

		<hr class="hr" />
		<div class="line space">
			<span class="label bold"> Delivery fee: </span>
			<span class="cost">
				₦{ops.cart.cost_delivery.toLocaleString()}
			</span>
		</div>
	</div>
</Content>

<Pay {ops} {total}></Pay>

<style>
	.page_title {
		margin: 24px 0;
	}

	.hr {
		margin: 24px 0;
	}

	.card {
		padding: 24px;
		border-radius: 8px;
		background-color: var(--bg1);
	}

	.label {
		font-size: 0.8rem;
	}
	.bold {
		font-weight: 800;
	}
	.cost {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}
</style>
