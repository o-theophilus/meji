<script>
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import Email_Admin from './status.delivered.email.admin.svelte';
	import Email_User from './status.delivered.email.user.svelte';
	let email_template_admin;
	let email_template_user;

	let form = $state({ comment: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		form.email_template_admin = email_template_admin.innerHTML.replace(/&amp;/g, '&');
		form.email_template_user = email_template_user.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let response = await fetch(
			`${import.meta.env.VITE_BACKEND}/orders/${module.value.order.key}/status/delivered`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.value.update(result.order);
			notify.open('Order Status Updated');
			module.close();
		} else {
			error = result;
		}
	};
</script>

<Form title="Update Order Status" error={error.error}>
	<Note>
		Please give reason for updating the order status to <span class="bold">"delivered"</span>
	</Note>

	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
	</div>
</Form>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={module.value.order} items={module.value.items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={module.value.order} items={module.value.items} />
</div>

<style>
	.bold {
		font-weight: bold;
		text-transform: capitalize;
	}
</style>
