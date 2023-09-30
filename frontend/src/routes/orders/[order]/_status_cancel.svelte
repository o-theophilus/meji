<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import SVG from '$lib/svg.svelte';
	import Info from '$lib/info.svelte';

	let note = '';
	let error = {};

	const validate = async () => {
		error = {};

		if (!note) {
			error.note = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		$loading = true;
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/order_status_cancel/${$module.order.key}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				},
				body: JSON.stringify({
					note
				})
			}
		);
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'order',
				data: resp.order
			};

			$module = {
				module: Info,
				status: 200,
				title: 'Order Canceled',
				message: 'Order has been Canceled',
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
		<b>Cancel Order </b>
	</svelte:fragment>

	<IG name="Note" label="Please give reason" {error} let:id>
		<textarea bind:value={note} {id} placeholder="Reason" />
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="hover_red" on:click={validate}>
		<SVG type="close" size="10" />
		Submit
	</Button>
</Form>

<style>
</style>
