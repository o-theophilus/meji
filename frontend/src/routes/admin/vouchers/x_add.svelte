<script>
	import { goto } from '$app/navigation';

	import { module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	let date = new Date();
	date.setDate(date.getDate() + 30);
	let day = date.getDate().toString();
	day = String(day).padStart(2, '0');
	let month = date.getMonth() + 1;
	month = String(month).padStart(2, '0');
	let year = date.getFullYear();

	let form = {
		validity: `${year}-${month}-${day}`
	};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.value) {
			error.value = 'This field is required';
		} else if (!Number.isInteger(form.value) || form.old_price < 1) {
			error.value = 'Please enter a valid value';
		}

		// if (!form.quantity) {
		// 	error.quantity = 'This field is required';
		// } else if (!Number.isInteger(form.quantity) || form.old_quantity < 1) {
		// 	error.quantity = 'Please enter a valid quantity';
		// }

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				goto(`/admin/voucher/${resp.data.voucher.key}`);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<svelte:head>
	<title>Add Voucher | Meji</title>
</svelte:head>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Voucher</div>
	</svelte:fragment>

	<svelte:fragment slot="info">
		<p>Add a new Voucher</p>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="value"> Value: </label>
			<input type="number" bind:value={form.value} id="value" placeholder="Value here" />
			{#if error.value}
				<p class="error">
					{error.value}
				</p>
			{/if}
		</div>

		<!-- <div class="inputGroup">
			<label for="quantity"> Quantity: </label>
			<input type="number" bind:value={form.quantity} id="quantity" placeholder="quantity here" />
			{#if error.quantity}
				<p class="error">
					{error.quantity}
				</p>
			{/if}
		</div> -->

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>
