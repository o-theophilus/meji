<script>
	import { user, module, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import Form from '$lib/module/form.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/module/info.svelte';

	let { order } = $module;
	let error = {};
	let value = order.info.account;

	const validate = async () => {
		error = {};

		if (!Number(value) && value != 0) {
			error.amount = 'invalid amount';
		} else if (value > $user.acc_balance) {
			error.amount = `amount larger than available balance (₦${$user.acc_balance.toLocaleString()})`;
		} else if (value > pay) {
			error.amount = `amount larger than total cost (₦${pay.toLocaleString()})`;
		} else if (value < 0) {
			error.amount = 'negative amount not allowed';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		order.info.account = value;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ value })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.order;

			$module = {
				module: Info,
				status: '200',
				title: '# Amount Changed',
				message: 'Amount has been changed successfully',
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};

	let pay = order.info.total_items + order.info.delivery_fee - order.info.account;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Account Amount</b>
		Enter amount to deduct from your account
	</svelte:fragment>

	<IG name="amount" {error} let:id>
		<input bind:value {id} type="number" placeholder="Amount here" />
	</IG>

	<Button class="primary" name="Ok" on:click={validate} />
</Form>

<style>
</style>
