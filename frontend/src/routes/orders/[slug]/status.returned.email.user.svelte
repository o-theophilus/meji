<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
	import Table from './_email.items_table.svelte';

	let { order, items } = $props();
</script>

<EmailTemplate>
	Dear {'{'}name{'}'},
	<br />
	<br />
	The order:
	<a
		style="text-decoration: none; color: #1d9bf0; text-transform: uppercase;"
		href="{page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key.substring(0, 8)}
	</a>
	Has been returned sucessfully.

	<Table {items} />
	<br />
	<br />

	We will process a refund according to out
	<a
		style="text-decoration: none; color: #1d9bf0;"
		href="{page.url.origin}/legal/terms#returns-and-refunds"
		target="_blank"
	>
		Terms & Conditions
	</a>

	 and renburse you within 3 days of
	receiving the returned item{items.length > 1 ? 's' : ''}

	<hr style="border-color: gray; margin: 24px 0;" />

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</EmailTemplate>
