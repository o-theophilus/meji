<script>
	import { days, months, ordinal_suffix_of } from '$lib/store.js';

	export let datetime;
	export let weekday = false;
	export let no_time = false;
	export let style = 0;

	$: if (datetime) {
		datetime = new Date(datetime);
	}
</script>

{#if datetime}
	<span class="date style_{style}">
		{#if weekday == 1}
			{days[datetime.getDay()]},
		{/if}

		{datetime.getDate()}-{months[datetime.getMonth()]}-{datetime.getFullYear()}

		{#if !no_time}
			{datetime.getHours().toString().padStart(2, '0')}:{datetime
				.getMinutes()
				.toString()
				.padStart(2, '0')}
		{/if}
	</span>
{/if}

<style>
	.style_1 {
		font-size: smaller;
		color: var(--ac3);
	}
</style>
