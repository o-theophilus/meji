<script>
	import { module, portal, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let note = '';
	let error = {};

	const validate = () => {
		error = {};

		if (!note) {
			error.note = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = `${$module.status == 'deleted' ? 'deleting' : 'deactivating'} . . .`;
		error = {};
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/status/${$module.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},

			body: JSON.stringify({
				status: $module.status,
				note
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				voucher: resp.voucher,
				logs: resp.logs
			};

			$module = '';
			$toast = {
				status: 200,
				message: `Voucher ${$module.status}`
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b> {$module.status == 'deleted' ? 'Delete' : 'Deactivate'} Voucher </b>
	</svelte:fragment>

	<IG
		name="note"
		label="Please give reason"
		{error}
		type="textarea"
		bind:value={note}
		placeholder="Reason"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button on:click={validate}>{$module.status == 'deleted' ? 'Delete' : 'Deactivate'}</Button>
</Form>

<style>
</style>
