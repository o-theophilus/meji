<script>
	import { user, currency, tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import Form from '$lib/module/form.svelte';

	export let data;
	let { order } = data;
	let error = '';
	let value = order.info.account;

	const validate = async () => {
		error = '';

		if (!Number(value) && value != 0) {
			error = 'invalid amount';
		} else if (value > $user.acc_balance) {
			error = `amount larger than available balance (${currency($user.acc_balance)})`;
		} else if (value > pay) {
			error = `amount larger than total cost (${currency(pay)})`;
		} else if (value < 0) {
			error = 'negative amount not allowed';
		}

		if (!error) {
			submit();
		}
	};

	const submit = async () => {
		order.info.account = value;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order_/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ value })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(order);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};

	let pay = order.info.total_items + order.info.delivery_fee - order.info.account;
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Account Amount</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">Enter amount to deduct from your account</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup horizontal">
			<label for="amount"> Amount: </label>
			<input type="number" bind:value id="amount" placeholder="Amount here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Ok" />
		</div>
	</form>
</Form>

<style>
</style>
