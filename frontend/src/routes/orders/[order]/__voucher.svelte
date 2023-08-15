<script>
	import { portal, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/module/form.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/module/info.svelte';

	let value = '';
	let error = {};

	const validate = async () => {
		error = {};

		if (!value) {
			error.code = 'This field is required';
		} else if (value.length != 10) {
			error.code = 'invalid code';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user_voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ code: value })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.order;

			$module = {
				module: Info,
				status: '200',
				title: '# Voucher Added',
				message: 'Voucher has been added successfully',
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
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Voucher Code</div>
	</svelte:fragment>

	<IG name="code" label="Voucher Code" {error} let:id>
		<input bind:value {id} type="text" placeholder="Voucher code here" />
	</IG>

	<Button name="Add" class="primary" on:click={validate} />
</Form>

<style>
</style>
